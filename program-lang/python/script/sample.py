#!/usr/bin/env python3

'''
'''
__author__ = "Huawen Yu"
__date__ = "Sep 13, 2020"

import os
import argparse

from base.common import BaseCommon, Common
from student.student import Student

class Sample:

    def __init__(self, args):
        """ctor."""
        self.common = BaseCommon(self, args)


    def run(self):
        stu = Student(self.common)
        stu.run()


# =============================================================================
if __name__ == "__main__":

    desc = f"Python script '{os.path.basename(__file__)}': A sample ..."
    print(desc)
    parser = argparse.ArgumentParser(description=desc)
    BaseCommon.add_arg_verbose(parser)

    default_repo_url = "https://svn.alfresco.com/repos/alfresco-open-mirror/integrations/GoogleDocs/HEAD/Google\ Docs\ Share/src/test/resources/alfresco/web-extensio"
    default_checkout_path = ""

    parser.add_argument("-r", "--repo_url", type=str, default=default_repo_url, dest="repo_url", help='Repository URL (default: "{default_repo_url}")' % default_repo_url)
    parser.add_argument("-l", "--local_path", type=str, default=default_checkout_path, dest="local_path", help='Local checkout path (default: "{default_checkout_path}")')

    default_username = getpass.getuser()
    parser.add_argument("-u", "--username", type=str, default=default_username, dest="svn_username", help='SVN login username (default: "%s")' % default_username)
    parser.add_argument("-p", "--password", type=str, dest="svn_password", help="SVN login password")

    args = parser.parse_args()

    sample = Sample(args)
    sample.run()

