'''
ssh assistance
'''
__author__ = "Huawen Yu"
__date__ = "Sep 13, 2020"

import re
import cmd2
import argparse
from cmdssh.dut.dut import Dut

# https://stackoverflow.com/questions/279237/import-a-module-from-a-relative-path
import os, sys, inspect
# realpath() will make your script run, even if you symlink it :)
cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)


from cmdssh.dut.dut import Dut
from base.common import *

class CmdSSH:

    def __init__(self, args):
        """ctor."""
        self.args = args


    @staticmethod
    def main(argv=sys.argv[1:]):
        # Detail explain:
        #  https://docs.python.org/dev/library/argparse.html
        prog = os.path.basename(__file__)
        desc = f"Python script '{prog}':\n"\
                " {prog} A sample..."

        usage = f"{prog} [options]:\n" \
                " {prog} -d 10.1.1.2 -u 'admin' -p '' \n" \
                " {prog} -d 10.1.1.2 -u 'admin' -p '' -t gdb:wad \n" \
                " {prog} -d 10.1.1.2 -u 'admin' -p '' -t log:wad,ips,urlfilter;show:wad \n"

        parser = argparse.ArgumentParser(description=desc, prog=prog, usage=usage)
        parser.add_argument("-e", "--command", help="command execute")
        parser.add_argument("-t", "--task", help="execute exist tasks")
        parser.add_argument("-n", "--dryrun", action="store_false",
                help="simulate dryrun, don't really send the command to target")
        parser.add_argument("-d", "--host", help="The target domain name or IP address", required=True)
        parser.add_argument("-u", "--username", help="The username used logon the target", required=True)
        parser.add_argument("-p", "--password", help="The password used logon the target")
        BaseCommon.add_arg_verbose(parser)

        args = parser.parse_args(argv)
        sys.argv = [sys.argv[0]]    # Clear the argv
        cmd1 = CmdSSH(args)
        cmd1.run()


    def run(self):
        act = Dut(self.args)
        act.run()


def main():
    CmdSSH.main()

if __name__ == "__main__":
    cmd1 = CmdSSH.main()

