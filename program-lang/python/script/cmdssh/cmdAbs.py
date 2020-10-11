import os
import re
import cmd2

from base.common import Common

class CommandAbs(cmd2.Cmd, Common):
    prompt = "(Cmd) "
    intro = "Abstract cmd layout."

    cmd_list = []

    codeDone   = 1
    codeExit   = 2
    codeFinish = 3

    def __init__(self, common: Common):
        #shortcuts = cmd2.DEFAULT_SHORTCUTS
        #shortcuts.update({'&': 'speak'})
        #super().__init__(multiline_commands=['orate'], shortcuts=shortcuts)
        cmd2.Cmd.__init__(self)
        Common.__init__(self, common)

        ## To hide built-in commands entirely, delete their "do_*" function from the cmd2.Cmd class
        self.hidden_commands += [
            'alias', 'edit', 'history', 'macro', 'py', 'run_pyscript', 'run_script', 'set', 'shell', 'shortcuts'
        ]

        # delete unused commands that are baked-into cmd2 and set some options
        #del cmd2.Cmd.do_py
        #del cmd2.Cmd.do_edit
        #del cmd2.Cmd.do_shortcuts
        #del cmd2.Cmd.do_pyscript
        #del cmd2.Cmd.do_set
        #del cmd2.Cmd.do_alias
        #del cmd2.Cmd.do_load
        cmd2.Cmd.abbrev = True
        self.allow_cli_args = False           # disable parsing of command-line args by cmd2
        self.allow_redirection = False        # disable redirection to enable right shift (>>) in custom_hash to work
        self.redirector = '\xff'              # disable redirection in the parser as well
        #self.shortcuts.update({'sh': 'show'}) # don't want "sh" to trigger the hidden "shell" command


    def _cmd_docmd(self, args):
        self.cmd_args = args
        cmds = self.get_all_commands()
        arg_list = args.split(' ')
        if arg_list:
            if arg_list[0] in cmds:
                return self.onecmd(args)


    def _cmd_doloop(self, subCmdObj):
        subCmdObj.cmdloop()
        if subCmdObj.exit_code == subCmdObj.codeDone:
            return self.do_done('all')
        elif subCmdObj.exit_code == subCmdObj.codeExit:
            return self.do_exit('all')


    def _cmd_subcmd(self, subCmdObj, args=''):
        if not args:
            return self._cmd_doloop(subCmdObj)
        elif args == '*':
            cmds = subCmdObj.get_all_commands()
            for cmdstr in cmds:
                subCmdObj._cmd_docmd(cmdstr)
        else:
            arg_list = args.split(' ')
            for cmdstr in arg_list:
                ret = subCmdObj._cmd_docmd(cmdstr)
                if subCmdObj.exit_code == self.codeFinish:
                    return self.do_done('all')
                elif subCmdObj.exit_code == self.codeDone:
                    return self.do_done('all')
                elif subCmdObj.exit_code == self.codeExit:
                    return self.do_exit('all')


    def _cmd_task(self, args):
        self.logger.debug(f'connect@args={args}')
        if not args:
            self.cmdloop()
        elif args == '*':
            cmds = self.get_all_commands()
            for cmdstr in cmds:
                self._cmd_docmd(cmdstr)
        else:
            ret = self._cmd_docmd(args)
            self.ctx.prepare_run_cmdlist()

            if self.exit_code == self.codeFinish:
                return self.do_done('all')
            elif self.exit_code == self.codeDone:
                return self.do_done('all')
            elif self.exit_code == self.codeExit:
                return self.do_exit('all')


    def _cmd_complete(self, subCmdObj, text):
        subcmds = subCmdObj.get_all_commands()
        subcmds2 = [
            subcmd for subcmd in subcmds
            if subcmd not in self.hidden_commands
            ]

        if text:
            return [
                subcmd for subcmd in subcmds2
                if subcmd.startswith(text)
            ]
        else:
            return subcmds2


    def cmdlist_append(self, args=''):
        if isinstance(args, str):
            self.cmd_list.append(args)
        elif isinstance(args, list):
            self.cmd_list.extend(args)
        #self.cmdlist_dump()


    def cmdlist_dump(self):
        import yaml
        #from pprint import pprint
        #self.poutput(pprint.pformat(self.cmd_list, indent=4))
        self.poutput(yaml.dump(self.cmd_list, default_flow_style=False))


    def _do_global(self):
        self.cmdlist_append([
                "end",
                "end",
                "end",
            ])
        if self.ctx.has_vdom():
            self.cmdlist_append([
                    "config global",
            ])

    def do_prompt(self, line):
        "Change the interactive prompt"
        self.prompt = line + ': '


    def do_dump(self, args):
        self.cmdlist_dump()


    def do_done(self, args):
        #self.poutput("Interact mode\n")
        self.exit_code = self.codeDone
        return True

    def do_exit(self, args):
        if args:
            # Exit the application
            if args == 'all':
                self.perror("Exiting ...")
                self.exit_code = self.codeExit
                return True
        return True

    def do_quit(self, args):
        return self.do_exit("all")
    do_EOF = do_quit

