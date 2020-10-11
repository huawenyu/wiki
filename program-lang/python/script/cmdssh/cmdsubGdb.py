import os
import re
import cmd2

from base.common import *
from cmdssh.cmdAbs import CommandAbs
from cmdssh.dut.state import StateCmd

class CmdGdb(CommandAbs):
    prompt = "(Cmd>>) "
    intro = "\nEnter gdb helper.\n"

    def __init__(self, common: Common):
        super().__init__(common)


    def complete_log(self, text, line, start_index, end_index):
        addresses = [
                'here@blubb.com',
                'foo@bar.com',
                'whatever@wherever.org',
                ]

        if text:
            return [
                address for address in addresses
                if address.startswith(text)
            ]
        else:
            return addresses


    def do_reset(self, args):
        self.cmdlist_append([
            "",
        ])


    def do_wad(self, args):
        self.logger.log(TRACE, f'{tag_yellow}@args={args}')
        self._do_global()

        if args and args.startswith("dis"):
            pass
        else:
            if self.ctx.dutInfo.VerNum2 < 56 and self.ctx.dutInfo.Product != 'FortiProxy':
                self.cmdlist_append([
                        "diag debug app wad -1",
                        "diag debug en",
                    ])
            else:
                self.cmdlist_append([
                        "diag debug dis",
                        "diag debug console no enable",
                        "diag debug console timestamp disable",
                        "diag ips debug disable all",
                        "diag wad debug clear",
                        "diag debug en",
                        "@sync",
                        # Process [1]: type=worker(2) index=0 pid=187 state=running
                        ("diag test app wad 1000",
                            r'Process.*?: type=(wanopt|worker).*? index=.*? pid=(.*?) state=.*?',
                            100,    # flush the old
                            ),
                        "@sync",
                        ('sys sh',
                            r'^/ # ', 'filter',
                            0,      # get the first match group
                            "gdbserver :444 --attach {grp2}"),
                    ])

            self.ctx.trans_state(StateCmd(self, self.ctx), self.ctx.cmd_list)
            self.exit_code = self.codeFinish


    def do_ips(self, args):
        self._do_global()

        if args.startswith("dis"):
            self.cmdlist_append([
                "diag debug dis",
                "diag ips debug disable all",
                ])
        else:
            if self.ctx.dutInfo.VerNum2 < 56 and self.ctx.dutInfo.Product != 'FortiProxy':
                pass
            else:
                self.cmdlist_append([
                        "diag ips debug enable all",
                        "diag ips debug disable timeout",
                        "#diag debug app ipsengine 0xeffeff",
                        "diag debug en",
                    ])


    def do_prompt(self, line):
        "Change the interactive prompt"
        self.prompt = line + ': '


