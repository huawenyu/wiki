import os
import re
import cmd2

from base.common import Common
from cmdssh.cmdAbs import CommandAbs

class CmdLog(CommandAbs):
    prompt = "(Cmd>>) "
    intro = "\nEnter diag helper.\n"

    def __init__(self, common: Common):
        super().__init__(common)


    def do_traffic(self, args):
        print(f"do log {args}")
        self.cmdlist_append("hello from wilson")
        self.cmdlist_dump()

    def do_utm(self, args):
        print(f"do log {args}")
        self.cmdlist_append("hello from wilson")
        self.cmdlist_dump()

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


    def do_debug(self, args):
        pass
        #sub_cmd = SubInterpreter()
        #sub_cmd.cmd_args = "world"
        #sub_cmd.cmdloop()


    def help_debug(self):
        print('\n'.join([ 'greet [person]',
            'Greet the named person',
            ]))


    def do_reset(self, args):
        self.cmdlist_append([
            "diag debug reset",
            "diag debug disable",
            "diag debug console no enable",
            "diag debug console timestamp disable",
            "diag ips debug disable all",
            "diag wad debug clear",
        ])


    def do_wad(self, args):
        self._do_global()

        if args.startswith("dis"):
            if self.ctx.dutInfo.VerNum2 < 56 and self.ctx.dutInfo.Product != 'FortiProxy':
                self.cmdlist_append([
                    "diag debug disable",
                    "diag debug app wad 0",
                ])
            else:
                self.cmdlist_append([
                    "diag debug disable",
                    "diag wad debug clear",
                    ])
        else:
            if self.ctx.dutInfo.VerNum2 < 56 and self.ctx.dutInfo.Product != 'FortiProxy':
                self.cmdlist_append([
                        "diag debug app wad -1",
                        "diag debug en",
                    ])
            else:
                self.cmdlist_append([
                        "diag wad debug enable level verbose",
                        "diag wad debug enable cat all",
                        "diag wad debug display pid enable",
                        "diag debug crash read",
                        "diag test app wad 2200",
                        "diag test app wad 3110",
                        "diag debug en",
                    ])


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


    def do_urlfilter(self, args):
        self._do_global()

        if args.startswith("dis"):
            self.cmdlist_append([
                "diag debug dis",
                "diag debug app urlfilter 0",
                ])
        else:
            if self.ctx.dutInfo.VerNum2 < 56 and self.ctx.dutInfo.Product != 'FortiProxy':
                pass
            else:
                self.cmdlist_append([
                        "diag debug app urlfilter -1",
                        "diag debug app foauthd -1",
                        "diag debug app ovrd -1",
                        "diagnose test application urlfilter 21",
                        "diagnose wad debug enable level verbose",
                        "diagnose wad debug enable cate detail",
                        "diagnose debug urlfilter src-addr 10.1.1.122",
                        "diag debug en",
                    ])

    def do_dns(self, args):
        self._do_global()

        if args.startswith("dis"):
            self.cmdlist_append([
                "diag debug dis",
                "diag debug app dnsproxy 0",
                ])
        else:
            if self.ctx.dutInfo.VerNum2 < 56 and self.ctx.dutInfo.Product != 'FortiProxy':
                pass
            else:
                self.cmdlist_append([
                        "diag debug app dnsproxy 3",
                        "diag debug en",
                    ])

    def do_cron(self, args):
        self._do_global()

        if args.startswith("dis"):
            self.cmdlist_append([
                "diag debug dis",
                "diag debug app forticron 0",
                ])
        else:
            if self.ctx.dutInfo.VerNum2 < 56 and self.ctx.dutInfo.Product != 'FortiProxy':
                pass
            else:
                self.cmdlist_append([
                        "diag debug app forticron 448",
                        "diag debug en",
                    ])


    def do_spam(self, args):
        self._do_global()

        if args.startswith("dis"):
            self.cmdlist_append([
                "diag debug dis",
                "diag debug app smtp 0",
                "diag debug app pop3 0",
                "diag debug app imap 0",
                "diag debug app scanunit 0",
                "diag debug app spamfilter 0",
                "diag debug app proxy 0",
                ])
        else:
            if self.ctx.dutInfo.VerNum2 < 56 and self.ctx.dutInfo.Product != 'FortiProxy':
                pass
            else:
                self.cmdlist_append([
                        "diag debug app smtp -1",
                        "diag debug app pop3 -1",
                        "diag debug app imap -1",
                        "diag debug app scanunit -1",
                        "diag debug app spamfilter -1",
                        "diag debug app proxy -1",
                        "diag debug en",
                    ])


    def do_gdb(self, args): print("do gdb")

    def do_prompt(self, line):
        "Change the interactive prompt"
        self.prompt = line + ': '


