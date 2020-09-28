#!/usr/bin/env python

'''
Implement svn checkout a dir recursively with break-continue
Require:
    $ sudo apt install python-svn
Usage:
    $ ./svnco.py -c -r "https://svn.apache.org/repos/asf/apr/apr-util/branches/1.7.x/"

'''

import os
import sys
import getpass
import pysvn
import pickle
import shutil
from collections import OrderedDict

__author__ = "Huawen Yu"
__date__ = "Sep 21, 2020"
# =============================================================================

from itertools import takewhile

class SvnClient:

    svnContinueDb      = '/tmp/svnclient_continue.db'      # local host path
    keyLocalParentPath = '/@path'      # local host path
    keySvnpath         = '/@url'       # remote svn url
    keySvnpath_isdir   = '/@isdir'     # is directory, or file
    keyProgress        = '/@progress'  # current progress
    keyStatus          = '/@status'    # 0 init, 1 pending, 2 done
    skipToRootPath     = 3             # jump to the #th of '/' in url: https://svn.apache.org/repos

    keyStatus_init     = 0
    keyStatus_pending  = 1
    keyStatus_done     = 2

    def __init__(self, args):
        self.args = args
        self.client = None
        self.cwd = os.getcwd()
        if self.args.repo_url.endswith('/'):
            self.args.repo_url = self.args.repo_url[:-1]
        self.pathtree = OrderedDict({
                self.keyStatus:          SvnClient.keyStatus_init,
                self.keySvnpath_isdir:   True,
                self.keyLocalParentPath: self.cwd,
                self.keySvnpath:         self.args.repo_url,
                })
        if self.args.local_path:
            self.coBasename = self.args.local_path
        else:
            self.coBasename = self.get_basename(self.args.repo_url)

    @staticmethod
    def dump_obj(obj, with_var=False):
        from pprint import pprint

        if with_var:
            pprint(vars(obj))
        else:
            pprint(obj)

    def rel_path(self, path):
        path = path.encode('ascii','ignore')
        find = path.find(self.args.repo_url)
        #print 'debug=', find, ' path=', path, ' repo=', self.args.repo_url
        if (find != -1):
            return (path, path[find+len(self.args.repo_url):])
        return (path, '')


    @staticmethod
    def get_basename(url):
        spath = SvnClient.find_nth(url, '/', SvnClient.skipToRootPath)
        return os.path.basename(url[spath:])


    @staticmethod
    def find_nth(haystack, needle, n):
        start = haystack.find(needle)
        while start >= 0 and n > 1:
            start = haystack.find(needle, start+len(needle))
            n -= 1
        return start


    @staticmethod
    def update_progress(progress):
        print '\r[{0}] {1}%'.format('#'*(progress/10), progress)


    def __load_path_tree(self):
        num = 1
        path_list = self.client.list(self.args.repo_url, recurse=True)
        maxLen = len(path_list)
        curLen = 0

        for path in path_list:
            curLen += 1
            objpath = path[0]
            has_props = objpath['has_props']

            # 'kind': <node_kind.dir>
            #SvnClient.dump_obj(objpath, True)
            #print objpath._PysvnDictBase__name
            (full_path, delta_path) = self.rel_path(objpath.path)

            num += 1
            if num > 30:
                break

            if has_props == 1:
                #print "Found props."
                pass

            curdir = self.pathtree
            parentPath = self.cwd
            lastBasename = self.coBasename
            dirs = delta_path.split(os.sep)
            if not dirs:
                continue

            end = len(dirs)
            for num, fdir in enumerate(dirs, start=1):
                if not fdir:
                    continue

                is_dir = False
                if num < end:
                    is_dir = True
                elif objpath.kind == pysvn.node_kind.dir:
                    is_dir = True

                #print fdir, type(fdir)
                #fdir = fdir.encode('ascii','ignore')
                if fdir in curdir:
                    curdir = curdir[fdir]
                    if is_dir:
                        if isinstance(parentPath, tuple):
                            parentPath = ''.join(parentPath)
                        parentPath = os.path.join(parentPath, lastBasename),
                        lastBasename = fdir
                else:
                    if is_dir:
                        if isinstance(parentPath, tuple):
                            parentPath = ''.join(parentPath)
                        pPath = os.path.join(parentPath, lastBasename)
                        newdir = OrderedDict({
                            self.keyStatus:          SvnClient.keyStatus_init,
                            self.keySvnpath_isdir:   True,
                            self.keyLocalParentPath: pPath,
                            self.keyProgress:        100 * curLen / maxLen,
                            self.keySvnpath:         full_path,
                            })

                        parentPath = pPath,
                        lastBasename = fdir
                    else:
                        if isinstance(parentPath, tuple):
                            parentPath = ''.join(parentPath)
                        pPath = os.path.join(parentPath, lastBasename)
                        newdir = OrderedDict({
                            self.keyStatus:          SvnClient.keyStatus_init,
                            self.keySvnpath_isdir:   False,
                            self.keyLocalParentPath: pPath,
                            self.keyProgress:        100 * curLen / maxLen,
                            })

                    curdir[fdir] = newdir
                    curdir = newdir

    def load_path_tree(self):
        print "Connect remote ..."
        print "  Start list all files, please wait ... ",
        sys.stdout.flush()

        if not self.load_continue():
            self.__load_path_tree()

        print "[DONE]!"
        sys.stdout.flush()

    def dump_path_tree(self):
        #print self.pathtree
        #SvnClient.dump_obj(dict(self.pathtree))
        import yaml

        yaml.add_representer(OrderedDict,
                lambda dumper, data: dumper.represent_mapping('tag:yaml.org,2002:map', data.items()))
        print(yaml.dump(self.pathtree))


    def remove(self, path):
        try:
            if os.path.isfile(path) or os.path.islink(path):
                os.remove(path)  # remove the file
            elif os.path.isdir(path):
                shutil.rmtree(path)  # remove dir and all contains
        except OSError:
            pass


    def _update_dir(self, fdirname, fdirInfo):
        # update dir
        if not isinstance(fdirInfo, dict):
            return
        if not fdirInfo.has_key(self.keySvnpath_isdir):
            return

        if fdirInfo[self.keySvnpath_isdir]:
            #basename = self.get_basename(fdirInfo[self.keySvnpath])
            #dstpath = os.path.join(fdirInfo[self.keyLocalParentPath], basename)

            if fdirname:
                if self.args.dryrun:
                    print 'update dir:', os.path.join(fdirInfo[self.keyLocalParentPath], fdirname)
                else:
                    updatePath = os.path.join(fdirInfo[self.keyLocalParentPath], fdirname)
                    if fdirInfo[self.keyStatus] != SvnClient.keyStatus_done:
                        self.remove(updatePath)
                        fdirInfo[self.keyStatus] = SvnClient.keyStatus_pending
                        self.client.update(os.path.join(fdirInfo[self.keyLocalParentPath], fdirname), depth=pysvn.depth.empty)
                        fdirInfo[self.keyStatus] = SvnClient.keyStatus_done
                        self.save_continue()

                    SvnClient.update_progress(fdirInfo[self.keyProgress])

            for child in fdirInfo:
                self._update_dir(child, fdirInfo[child])
        # update files
        elif fdirname:
            if self.args.dryrun:
                print 'update fil:', os.path.join(fdirInfo[self.keyLocalParentPath], fdirname)
            else:
                updatePath = os.path.join(fdirInfo[self.keyLocalParentPath], fdirname)
                if fdirInfo[self.keyStatus] != SvnClient.keyStatus_done:
                    self.remove(updatePath)
                    fdirInfo[self.keyStatus] = SvnClient.keyStatus_pending
                    self.client.update(os.path.join(fdirInfo[self.keyLocalParentPath], fdirname))
                    fdirInfo[self.keyStatus] = SvnClient.keyStatus_done
                    self.save_continue()

                SvnClient.update_progress(fdirInfo[self.keyProgress])


    def check_continue(self):
        if self.args.resume:
            if os.path.isfile(self.svnContinueDb):
                with open(self.svnContinueDb, "rb") as f:
                    return True
        return False


    def clean(self):
        print "Clean", self.coBasename, "all, exit."
        self.remove(os.path.join(self.cwd, self.coBasename))
        self.remove(self.svnContinueDb)

    def load_continue(self):
        if self.check_continue():
            with open(self.svnContinueDb, "rb") as f:
                self.pathtree = pickle.load(f)
                return True
        return False


    def save_continue(self):
        if self.args.resume:
            with open(self.svnContinueDb, "wb") as f:
                pickle.dump(self.pathtree, f)


    def traverse_checkout(self):
        if self.args.dryrun:
            print 'checkout  :', self.args.repo_url, 'into', os.path.join(self.cwd, self.coBasename)
        elif self.check_continue():
            self.client.cleanup(os.path.join(self.cwd, self.coBasename))
        else:
            self.client.checkout(self.args.repo_url, os.path.join(self.cwd, self.coBasename), depth=pysvn.depth.empty)

        # Support continue start after the checkout of top-dir
        self.save_continue()
        self._update_dir(None, self.pathtree)
        self.save_continue()


    def getSvnClient(self):

        password = self.args.svn_password
        if not password:
            password = getpass.getpass('Enter SVN password for user "%s": ' % self.args.svn_username)

        client = pysvn.Client()
        client.callback_get_login = lambda realm, username, may_save: (True, self.args.svn_username, password, True)

        #client.set_default_username( username )
        #client.set_default_password( password )
        self.client = client

    def checkout(self):
        if self.args.clean:
            self.clean()
        else:
            client.getSvnClient()
            client.load_path_tree()
            if self.args.dryrun:
                client.dump_path_tree()
            client.traverse_checkout()


# =============================================================================
if __name__ == "__main__":

    from optparse import OptionParser
    usage = """%prog -r url """

    # https://apr.apache.org/anonsvn.html
    default_repo_url = "https://svn.apache.org/repos/asf/apr/apr-util/branches/1.7.x/"
    #default_repo_url = "https://svn.apache.org/repos/asf/apr/apr-util/branches/1.7.x/build"
    default_co_path = ""

    parser = OptionParser(usage)
    parser.add_option("-r", "--repo_url", type="str", default=default_repo_url, dest="repo_url", help='[Must] Repository URL (default: "%s")' % default_repo_url)
    parser.add_option("-l", "--local_path", type="str", default=default_co_path, dest="local_path", help='[Option] Local checkout directory (like: "%s")' % SvnClient.get_basename(default_repo_url))

    default_username = getpass.getuser()
    parser.add_option("-u", "--username", type="str", default=default_username, dest="svn_username", help='SVN login username (default: "%s")' % default_username)
    parser.add_option("-p", "--password", type="str", dest="svn_password", help="SVN login password")

    parser.add_option("-v", "--verbose", action="store_true", default=False, dest="verbose", help="Verbose output")
    parser.add_option("-n", "--dryrun", action="store_true", default=False, dest="dryrun", help="Dryrun")
    parser.add_option("-c", "--resume", action="store_true", default=True, dest="resume", help="Support continue checkout for instable network")
    parser.add_option("-d", "--clean&delete", action="store_true", default=False, dest="clean", help="Clean")

    (options, args) = parser.parse_args()

    client = SvnClient(options)
    client.checkout()

