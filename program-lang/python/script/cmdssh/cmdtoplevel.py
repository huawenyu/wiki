import os
import re
import cmd2

from base.common import *
from cmdssh.cmdAbs import CommandAbs
from cmdssh.cmdsubLog import CmdLog
from cmdssh.cmdsubGdb import CmdGdb

class CmdTopLevel(CommandAbs):
    prompt = "(Cmd>) "
    intro = "\nEnter cmd helper.\n"

    def __init__(self, common: Common):
        super().__init__(common)

        # Make settable at runtime
        self.cmd_args = None


    def do_log(self, args=''):
        return self._cmd_subcmd(CmdLog(self), args)

    def complete_log(self, text, line, start_index, end_index):
        return self._cmd_complete(CmdLog(self), text)

    def do_debug(self, args):
        pass
        #sub_cmd = SubInterpreter()
        #sub_cmd.cmd_args = "world"
        #sub_cmd.cmdloop()

    def help_debug(self):
        print('\n'.join([ 'greet [person]',
            'Greet the named person',
            ]))

    def do_gdb(self, args):
        self.logger.log(TRACE, f'{tagString}@args={args}')
        return self._cmd_subcmd(CmdGdb(self), args)


    def do_prompt(self, line):
        "Change the interactive prompt"
        self.prompt = line + ': '


