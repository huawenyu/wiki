
import os
import re
import sys
import cmd2
import uuid
import pexpect

from base.common import *
from base.data import EventExit, EventDelay
from cmdssh.dut.info import DutType, DutInfo

class State(Common):
    DutStateInit    = "init"
    DutStatePrompt  = 'prompt'
    DutStateInfo    = 'info'
    DutStateCmd     = 'cmd'
    DutStateTask    = 'task'     # parse task and execute them
    DutStatePass    = 'pass'     # interact mode
    DutStateMatcher = 'match'    # matched -> cb

    matchByState    = 'state'    # default
    matchByFilter   = 'filter'   # output_filter return by '\r', sometime no '\r' like: 'sys sh'

    def __init__(self, name, common, ctx):
        """ctor."""
        super().__init__(common)
        self.name = name
        self.ctx = ctx

    def is_filter(self):
        pass

    def init_cmds(self, next_cmds):
        pass

    def parse_line(self, line, next_cmds):
        pass

    def cmd_sync(self):
        uid = uuid.uuid1()  # creating UUID
        uuid_str = str(uid.hex)
        echostr = self.ctx.dutType.echoStr()
        return (f'{echostr} "{uuid_str}"', rf'{uuid_str}')


class StateInit(State):
    def __init__(self, common, ctx):
        """ctor."""
        super().__init__(State.DutStateInit, common, ctx)
        self.substate = 0


    def is_filter(self):
        return True

    def init_cmds(self, next_cmds):
        pass


    def parse_line(self, line, next_cmds):
        self.logger.log(DEBUG, f"{line}")
        if not line:
            return True
        self.ctx.trans_state(StatePrompt(self, self.ctx), next_cmds)
        return False


class StatePrompt(State):
    rePromptLinux = re.compile(r'^.*( \S+ )$')
    rePromptKVM   = re.compile(r'(.* # )')

    def __init__(self, common, ctx):
        """ctor."""
        super().__init__(State.DutStatePrompt, common, ctx)
        self.substate = 0

    def is_filter(self):
        return True

    def init_cmds(self, next_cmds):
        next_cmds.append('')

    def parse_line(self, line, next_cmds):
        """
        >>> m = re.search('^.*( \S+ )$', 'mint@linuxmint-17 ~ $ ')
        >>> m.group(1)
        ' $ '
        >>> m = re.search('^.*( \S+ )$', 'FortiGate-VM64-KVM # ')
        >>> m.group(1)
        ' # '

        # match prompt like: 'FortiGate-VM64-KVM # '
        >>> host = 'FortiGate-VM64-KVM'
        >>> # prompt1 = r"^FortiGate-VM64-KVM #"
        >>> prompt1 = r"^" + re.escape(host) + r" # "
        >>> m = re.search(prompt1, 'FortiGate-VM64-KVM # ')
        >>> m.group()
        'FortiGate-VM64-KVM # '

        # match prompt like: 'FortiGate-VM64-KVM (root) # '
        >>> prompt2 = r"^" + re.escape(host) + r" \(\w+?\) # "
        >>> m = re.search(prompt2, 'FortiGate-VM64-KVM (root) # ')
        >>> m.group()
        'FortiGate-VM64-KVM (root) # '
        """
        #
        # Set command prompt to something more unique.
        #
        self.logger.log(INFO, f'os={str(self.ctx.dutType.osType)}: {line}')
        if self.ctx.dutType.osType == DutType.Dummy:
            return False
        elif self.ctx.dutType.osType == DutType.Linux:
            if self.substate == 0:
                self.substate = 1
                next_cmds.append('bash')
                next_cmds.append("PS1='=PEXPECT= # '")
                return False
            elif self.substate == 1:
                self.substate = 2
                next_cmds.append("set prompt='=PEXPECT= # '")
                return False
            elif self.substate == 2:
                self.substate = 3
                next_cmds.append("set prompt='=PEXPECT= # '")
                m = self.rePromptLinux.search(line)
                if m:
                    self.ctx.dutInfo.Prompt = m.group(1)
                    self.ctx.trans_state(StateInfo(self, self.ctx), next_cmds)
                    return False
                else:
                    next_cmds.append('')
                    return False
            elif self.substate == 3:
                self.logger.log(INFO, f'os={self.ctx.dutType.osType}: guess prompt fail, use default')
                self.ctx.dutInfo.Prompt = "=PEXPECT= # "
                self.ctx.trans_state(StateInfo(self, self.ctx), next_cmds)
                return False
        elif self.ctx.dutType.osType == DutType.DutFOS:
            if self.substate == 0:
                m = self.rePromptKVM.search(line)
                if m:
                    self.ctx.dutInfo.Prompt = m.group(1)
                    self.logger.log(DEBUG, f"  Guess prompt: '{self.ctx.dutInfo.Prompt}'")
                    self.ctx.trans_state(StateInfo(self, self.ctx), next_cmds)
                    return False
                else:
                    self.substate = 1
                    next_cmds.append('')
                    self.logger.log(DEBUG, f"  Guess prompt fail")
                    return False
            elif self.substate == 1:
                m = self.rePromptKVM.search(line)
                if m:
                    self.ctx.dutInfo.Prompt = m.group(1)
                    self.logger.log(DEBUG, f"  Guess prompt: '{self.ctx.dutInfo.Prompt}'")
                    self.ctx.trans_state(StateInfo(self, self.ctx), next_cmds)
                    return False
                else:
                    self.substate = 2
                    self.ctx.trans_state(StateInfo(self, self.ctx), next_cmds)
                    return False
        else:
            return False


class StateInfo(State):
    reVersion   = re.compile(r'Version: (.*?)-(.*?) v(.*?),build(.*?),(.*?) (.*?)')
    reSerial    = re.compile(r"Serial-Number: (.*)")
    reLogdisk   = re.compile(r"Log hard disk: (.*)")
    reHost      = re.compile(r"Hostname: (.*)")
    reOperation = re.compile(r"Operation Mode: (.*)")
    reVdom      = re.compile(r"Virtual domain configuration: (.*)")
    reHAmode    = re.compile(r"Current HA mode: (.*)")
    reSystime   = re.compile(r"System time: (.*)")

    def __init__(self, common, ctx):
        """ctor."""
        super().__init__(State.DutStateInfo, common, ctx)
        self.substate = 0

    def is_filter(self):
        return True


    def init_cmds(self, next_cmds):
        if self.ctx.dutType.osType == DutType.DutFOS:
            next_cmds.append("get system status")


    def parse_line(self, line, next_cmds):
        if self.substate == 0:
            res = self.reVersion.match(line)
            if res:
                self.substate = 1
                self.ctx.dutInfo.Product = res.group(1)
                self.ctx.dutInfo.Model = res.group(2)
                self.ctx.dutInfo.Version = res.group(3)
                self.ctx.dutInfo.VerNum = int(self.ctx.dutInfo.Version.replace(".", ""))
                self.ctx.dutInfo.VerNum2 = int(self.ctx.dutInfo.VerNum / 10)
                self.ctx.dutInfo.BuildNum = res.group(4)
                self.ctx.dutInfo.BuildDate = res.group(5)
                return True
        elif self.substate == 1:
            res = self.reSerial.match(line)
            if res:
                self.substate = 2
                self.ctx.dutInfo.ModelSN = res.group(1)
                return True
        elif self.substate == 2:
            res = self.reLogdisk.match(line)
            if res:
                self.substate = 3
                self.ctx.dutInfo.LogDisk = res.group(1)
                return True
        elif self.substate == 3:
            res = self.reHost.match(line)
            if res:
                self.substate = 4
                self.ctx.dutInfo.Hostname = res.group(1)
                return True
        elif self.substate == 4:
            res = self.reOperation.match(line)
            if res:
                self.substate = 5
                self.ctx.dutInfo.OperationMode = res.group(1)
                return True
        elif self.substate == 5:
            res = self.reVdom.match(line)
            if res:
                self.substate = 6
                self.ctx.dutInfo.Vdom = res.group(1)
                return True
        elif self.substate == 6:
            res = self.reHAmode.match(line)
            if res:
                self.substate = 7
                self.ctx.dutInfo.HAmode = res.group(1)
                return True
        elif self.substate == 7:
            res = self.reSystime.match(line)
            if res:
                self.substate = 8
                self.ctx.dutInfo.SystemTime = res.group(1)
                self.ctx.child.sendline('')
                return True
        elif self.substate == 8:
            if re.search(rf"^{self.ctx.dutInfo.Prompt}$", line):
                self.substate = 100
                self.ctx.trans_state(StateTask(self, self.ctx), next_cmds)
                self.logger.log(INFO, f'dutInfo: {str(self.ctx.dutInfo)}')
                return False

        # Continue match the following lines
        return True


class StateTask(State):

    def __init__(self, common, ctx):
        """ctor."""
        super().__init__(State.DutStateTask, common, ctx)
        if self.args.task:
            self.ctx.child.sendline('')     # trigger

    def init_cmds(self, next_cmds):
        pass


    def is_filter(self):
        return True


    def parse_line(self, line, next_cmds):
        self.logger.log(INFO, f'{line}')
        if self.args.task:
            self.ctx.topCmd._cmd_task(self.args.task)
        return True



class StatePass(State):

    def __init__(self, common, ctx):
        """ctor."""
        super().__init__(State.DutStatePass, common, ctx)


    def init_cmds(self, next_cmds):
        pass

    def is_filter(self):
        return False


    def parse_line(self, line, next_cmds):
        self.logger.log(INFO, f'{line}')
        return True


class StateCmd(State):

    # (pre, match, then-action)
    # (None, r'KVM-125 # ', <which-match-group>, "diag test app wad 1000")
    #                       0  the first match group
    #                       -1 current match group
    #                       -2 last match group
    #                      >90 flush old, the index=<idx> - 100
    subStateInit    = 'subInit'
    subStateExpect  = 'subExpect'
    subStateExecute = 'subExecute'

    def __init__(self, common, ctx):
        """ctor."""
        super().__init__(State.DutStateCmd, common, ctx)
        self.substate = self.subStateInit
        self.matched_res = []

        self.currCmd = None
        self.currPre = None
        self.currMatch = None
        self.currMatchBy = None
        self.currGrpIdx = None
        self.currAction = None


    def is_filter(self):
        return True

    def take_action(self, line, next_cmds):
        try:
            res = self.matched_res[self.currGrpIdx]
        except IndexError:
            self.logger.log(WARNING, f'Get match-group index error: {self.currGrpIdx}')
            self.ctx.child.sendline(self.currAction)
            return

        grp1 = ''
        grp2 = ''
        grp3 = ''
        self.logger.log(INFO, f'matched {self.currGrpIdx} as: {res.groups()}')
        grpNum = len(res.groups())
        if grpNum == 1:
            grp1 = res.group(1)
        elif grpNum == 2:
            grp1 = res.group(1)
            grp2 = res.group(2)
        elif grpNum == 3:
            grp1 = res.group(1)
            grp2 = res.group(2)
            grp3 = res.group(3)

        self.substate = self.subStateExecute
        template_vals = {
                'grp1': grp1,
                'grp2': grp2,
                'grp3': grp3,
                }
        cmdstr = self.currAction.format(**template_vals)
        self.ctx.child.sendline(cmdstr)

    def parse_line(self, line, next_cmds):
        self.logger.log(TRACE, f'{self.substate} do {self.currCmd} {self.ctx.cmd_list}')
        if self.substate == self.subStateExpect and self.currCmd:
            matcher = re.compile(self.currMatch)
            res = matcher.match(line)
            if not res:
                self.logger.log(TRACE2, f'no match, wait ...')
                return True     # continue wait

            # Store matcher
            self.logger.log(DEBUG, f'matched {self.currGrpIdx} as: {res.groups()}')
            if self.currGrpIdx >= 90:
                self.matched_res.clear()    # flush all before store
                self.currGrpIdx -= 100
            self.matched_res.append(res)

            if self.currAction:
                self.take_action(line, next_cmds)

        while self.ctx.cmd_list:
            self.currCmd = self.ctx.cmd_list.pop(0)
            if isinstance(self.currCmd, str):
                if self.currCmd == "@sync":
                    self.currCmd = self.cmd_sync()
                elif self.currCmd.startswith("@delay"):
                    self.ctx.que.put(EventDelay(1, self.currCmd[6:]))
                    continue

            if isinstance(self.currCmd, tuple):
                cmdLen = len(self.currCmd)
                self.currMatchBy = None
                self.currGrpIdx = 0
                self.currAction = None

                if cmdLen == 2:
                    self.currPre, self.currMatch = self.currCmd
                elif cmdLen == 3:
                    self.currPre, self.currMatch, self.currGrpIdx = self.currCmd
                elif cmdLen == 4:
                    self.currPre, self.currMatch, self.currGrpIdx, self.currAction = self.currCmd
                elif cmdLen == 5:
                    self.currPre, self.currMatch, self.currMatchBy, self.currGrpIdx, self.currAction = self.currCmd
                else:
                    self.logger.log(ERROR, f'cmd touple error: {self.currCmd}')
                    return True

                if self.currMatch:
                    self.substate = self.subStateInit
                    if self.currPre: # pre
                        self.substate = self.subStateExpect
                        if self.currMatchBy and self.currMatchBy == self.matchByFilter:
                            self.ctx.set_matcher(self.currMatch)

                        self.ctx.child.sendline(self.currPre)
                        return True     # do-expect-then-next
                else:   # If no matcher, regress back to simple cmdstr
                    if self.currPre:
                        self.ctx.child.sendline(self.currPre)
                    if self.currAction:
                        self.take_action(line, next_cmds)
            else:
                self.substate = self.subStateExecute
                self.ctx.child.sendline(self.currCmd)
                # continue next cmd

        self.ctx.trans_state(StatePass(self, self.ctx), next_cmds)
        return True


