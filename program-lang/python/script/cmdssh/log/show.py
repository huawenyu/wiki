import os
import re
import cmd2
import pexpect

from base.common import Common

class MyInterpreter(cmd2.Cmd):
    prompt = "(level1) "
    intro = "Simple command processor example."

    def __init__(self):
        #shortcuts = cmd2.DEFAULT_SHORTCUTS
        #shortcuts.update({'&': 'speak'})
        #super().__init__(multiline_commands=['orate'], shortcuts=shortcuts)
        super().__init__()

        # Make settable at runtime
        self.cmd_args = None

    def try_parse_cmd(self, args):
        print(f"args={args}")
        self.cmd_args = args
        cmds = self.get_all_commands()
        if args in cmds:
            return self.onecmd(args)


    def do_level1(self, args):
        print("do level1")

    def do_level2(self, args):
        sub_cmd = SubInterpreter()
        sub_cmd.cmd_args = "world"
        sub_cmd.cmdloop()

    def help_level2(self):
        print('\n'.join([ 'greet [person]',
            'Greet the named person',
            ]))

    #def parseline(self, line):
    #    ret = cmd2.Cmd.parseline(self, line)
    #    print(f'parseline({line}) => {ret}')
    #    return ret
    #
    #def onecmd(self, s):
    #    print 'onecmd(%s)' % s
    #    return cmd.Cmd.onecmd(self, s)

    def do_level3(self, args):
        print("do level3")

    def do_prompt(self, line):
        "Change the interactive prompt"
        self.prompt = line + ': '

    def do_quit(self, args):
        print("Exit\n")
        return True
    do_EOF = do_quit

