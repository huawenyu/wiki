#!/usr/bin/env python

'''
This script makes a sparse checkout of an SVN tree in the current working directory.
    $ sudo apt install python-svn

Given a list of paths in an SVN repository, it will:
1. Checkout the common root directory
2. Update with depth=empty for intermediate directories
3. Update with depth=infinity for the leaf directories
'''

import os
import getpass
import pysvn

__author__ = "Karl Ostmo"
__date__ = "July 13, 2011"

# =============================================================================

# XXX The os.path.commonprefix() function does not behave as expected!
# See here: http://mail.python.org/pipermail/python-dev/2002-December/030947.html
# and here: http://nedbatchelder.com/blog/201003/whats_the_point_of_ospathcommonprefix.html
# and here (what ever happened?): http://bugs.python.org/issue400788
from itertools import takewhile
def allnamesequal(name):
    return all(n==name[0] for n in name[1:])

def commonprefix(paths, sep='/'):
    bydirectorylevels = zip(*[p.split(sep) for p in paths])
    return sep.join(x[0] for x in takewhile(allnamesequal, bydirectorylevels))

# =============================================================================
def getSvnClient(options):

    password = options.svn_password
    if not password:
        password = getpass.getpass('Enter SVN password for user "%s": ' % options.svn_username)

    client = pysvn.Client()
    client.callback_get_login = lambda realm, username, may_save: (True, options.svn_username, password, True)
    return client

# =============================================================================
def sparse_update_with_feedback(client, new_update_path):
    revision_list = client.update(new_update_path, depth=pysvn.depth.empty)

# =============================================================================
def sparse_checkout(options, client, repo_url, sparse_path, local_checkout_root):

    path_segments = sparse_path.split(os.sep)
    path_segments.reverse()

    if options.verbose:
        print "sparse_path:", sparse_path
        print "path_segments:", path_segments
    # Update the middle path segments
    new_update_path = local_checkout_root
    while len(path_segments) > 1:
        path_segment = path_segments.pop()
        new_update_path = os.path.join(new_update_path, path_segment)
        sparse_update_with_feedback(client, new_update_path)
        if options.verbose:
            print "Added internal node:", path_segment

    # Update the leaf path segment, fully-recursive
    leaf_segment = path_segments.pop()
    new_update_path = os.path.join(new_update_path, leaf_segment)

    if options.verbose:
        print "Will now update with 'recursive':", new_update_path
    update_revision_list = client.update(new_update_path)

    if options.verbose:
        for revision in update_revision_list:
            print "- Finished updating %s to revision: %d" % (new_update_path, revision.number)

# =============================================================================
def group_sparse_checkout(options, client, repo_url, sparse_path_list, local_checkout_root):
    if not sparse_path_list:
        print "Nothing to do!"
        return

    checkout_path = None
    if len(sparse_path_list) > 1:
        checkout_path = commonprefix(sparse_path_list)
    else:
        checkout_path = sparse_path_list[0].split(os.sep)[0]

    root_checkout_url = os.path.join(repo_url, checkout_path).replace("\\", "/")
    revision = client.checkout(root_checkout_url, local_checkout_root, depth=pysvn.depth.empty)

    print 'wilson', checkout_path
    checkout_path_segments = checkout_path.split(os.sep)
    for sparse_path in sparse_path_list:

        # Remove the leading path segments
        path_segments = sparse_path.split(os.sep)
        start_segment_index = 0
        for i, segment in enumerate(checkout_path_segments):
            if segment == path_segments[i]:
                start_segment_index += 1
            else:
                break

        if start_segment_index > 1:
            pruned_path = os.sep.join(path_segments[start_segment_index:])
        else:
            pruned_path = os.sep.join(path_segments)
        print 'wilson', pruned_path, " segs", path_segments
        sparse_checkout(options, client, repo_url, pruned_path, local_checkout_root)

# =============================================================================
if __name__ == "__main__":

    from optparse import OptionParser
    usage = """%prog  [path2] [more paths...]"""

    default_repo_url = "http://svn.example.com/MyRepository"
    default_checkout_path = "sparse_trunk"

    parser = OptionParser(usage)
    parser.add_option("-r", "--repo_url", type="str", default=default_repo_url, dest="repo_url", help='Repository URL (default: "%s")' % default_repo_url)
    parser.add_option("-l", "--local_path", type="str", default=default_checkout_path, dest="local_path", help='Local checkout path (default: "%s")' % default_checkout_path)

    default_username = getpass.getuser()
    parser.add_option("-u", "--username", type="str", default=default_username, dest="svn_username", help='SVN login username (default: "%s")' % default_username)
    parser.add_option("-p", "--password", type="str", dest="svn_password", help="SVN login password")

    parser.add_option("-v", "--verbose", action="store_true", default=False, dest="verbose", help="Verbose output")
    (options, args) = parser.parse_args()

    client = getSvnClient(options)
    group_sparse_checkout(
        options,
        client,
        options.repo_url,
        map(os.path.relpath, args),
        options.local_path)

