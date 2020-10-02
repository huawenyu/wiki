'''
ssh assistance
'''
__author__ = "Huawen Yu"
__date__ = "Sep 13, 2020"

import re
import cmd2
import argparse

# https://stackoverflow.com/questions/279237/import-a-module-from-a-relative-path
import os, sys, inspect
# realpath() will make your script run, even if you symlink it :)
cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)


from base.common import Common, BaseCommon
from cmdssh.interact import Interact

class CmdSSH:

    def __init__(self, args):
        """ctor."""
        self.common = BaseCommon(self, args)


    def run(self):
        act = Interact(self.common)
        act.run()


if __name__ == "__main__":

    desc = f"Python script '{os.path.basename(__file__)}': A sample ..."
    print(desc)
    parser = argparse.ArgumentParser(description=desc)
    BaseCommon.add_arg_verbose(parser)

    args = parser.parse_args()
    cmd1 = CmdSSH(args)
    cmd1.run()


