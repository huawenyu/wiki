import os
import re
import sys
import cmd2
import time
import pexpect
import threading
from queue import Queue, Empty

from base.common import *
from base.data import EventExit, EventDelay
from cmdssh.cmdtoplevel import CmdTopLevel
from cmdssh.dut.state import StateInit, StateCmd
from cmdssh.dut.info import DutType, DutInfo


class EventThread(threading.Thread):
    def __init__(self, que, ctx, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super().__init__()
        self.target = target
        self.name = name
        self.que = que
        self.ctx = ctx
        self.topCmd = None
        return

    def run(self):
        while True:
            if not self.que.empty():
                evt = self.que.get()
                self.ctx.logger.log(INFO, f"thread evt{evt}")
                if isinstance(evt, EventExit):
                    break       # exit thread
                elif isinstance(evt, EventDelay):
                   time.sleep(evt.seconds)
                   self.ctx.child.sendline(evt.cmdstr)
        return


class Dut(Common):

    def __init__(self, args):
        """ctor."""
        common = BaseCommon(self, args)
        super().__init__(common)

        self.state = StateInit(common, self)
        self.oldstate = self.state
        self.dutType = DutType("default", DutType.DutFOS, "unknown")
        self.dutInfo = DutInfo("dummy")
        self.cmd_list = []
        self.que = Queue(10)
        self.alive = '/tmp/pyscript'

        self.outfilter_buf = ''
        self.filter_matcher = None
        self.next_cmds = []

    def trans_state(self, state, next_cmds):
        self.logger.log(INFO, f"Transfer: from {self.state.name} to {state.name}")
        if self.state.name != state.name:
            state.init_cmds(next_cmds)
        self.oldstate = self.state
        self.state = state


    def rollback_state(self, next_cmds):
        self.logger.log(INFO, f"Rollback: from {self.state.name} to {self.oldstate.name}")
        self.state = self.oldstate


    def set_matcher(self, matchstr):
        self.logger.log(INFO, f"filter-match: '{matchstr}'")
        self.filter_matcher = re.compile(matchstr)


    def has_vdom(self):
        return self.dutInfo.has_vdom()


    def get_command(self):
        """
        >>> me.get_command("telnet", "host", "user", "pass")
        'telnet user@host'
        >>> me.get_command("ssh", "host", "user", "pass")
        'ssh -qo "StrictHostKeyChecking=no" user@host'
        >>> me.get_command('ssh -qo "StrictHostKeyChecking=no"', "host", "user", "pass")
        'ssh -qo "StrictHostKeyChecking=no" user@host'
        >>> me.get_command("ssh -qo 'StrictHostKeyChecking=no'", "host", "user", "pass")
        "ssh -qo 'StrictHostKeyChecking=no' user@host"
        """
        # ssh_command = 'ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -p {} {}@{}'.format(karaf_port, karaf_id, karaf_host)
        if not self.args.command:
            self.args.command = "ssh"
        if self.args.command.startswith("ssh"):
            if -1 == self.args.command.find("StrictHostKeyChecking"):
                command = self.args.command.replace("ssh", 'ssh -qo "StrictHostKeyChecking=no" -o "UserKnownHostsFile /dev/null"')
        return command + " " + self.args.username + "@" + self.args.host


    def connect(self):
        filter_buf = ''
        input_buf = ''
        filter_buf_size = 256
        let_me_out = False
        bash_prompt = re.compile('bash-[.0-9]+[$#] $')

        cmdStr = self.get_command()
        self.logger.log(INFO, f"{tag_blink}{cmdStr}")

        #self.child = pexpect.spawn('bash --noprofile --norc')
        self.child = pexpect.spawn(cmdStr, echo=True)
        #self.child = PopenSpawn(command, timeout=5)    # can't interact()

        # Delay used before sending data to child. Time in seconds.
        # Most Linux machines don't like this to be below 0.03 (30 ms).
        #self.child.delaybeforesend = 0.05
        self.child.delaybeforesend = None
        self.child.setwinsize(2048, 2048)


    def get_info(self):
        self.state = self.DutStateInfo;
        cmdStr = self.dutType.getinfoStr()
        self.child.sendline(cmdStr)

    def tigger_outputfilter(self):
        while os.path.exists(f'{self.alive}'):
            try:
                line = self.que.get(timeout=0.3)   # get_nowait()
            except Empty:
                pass
            except Exception as e:
                self.logger.log(ERROR, f"thread exception: {str(e)}")
            else:
                if line == 'TriggerOutfilter':
                    if self.child and not self.child.isalive():
                        self.child.sendline('')


    def run(self):

        self.connect()
        self.child.sendline('')    # trigger output_filter
        #self.que.put('TriggerOutfilter')
        pid = os.getpid()
        self.alive += '.' + str(pid)
        os.system(f'touch {self.alive}')

        #t1 = threading.Thread(target=self.tigger_outputfilter)
        #t1.setDaemon(True)
        #t1.start()

        #thEvent = EventThread(self.que, self, name='consumer')
        #thEvent.setDaemon(True)
        #thEvent.start()

        while True:
            if self.child and not self.child.isalive():
            # Default: <C-]> exit the interact mode, then into the command mode
                self.child.close()
                self.connect()

            self.topCmd = CmdTopLevel(self)
            # Default: <C-]> exit the interact mode, then into the command mode
            self.child.interact(input_filter=None, output_filter=self.output_filter)
            self.topCmd.cmdloop()

            self.prepare_run_cmdlist()
            if self.cmd_list and not self.filter_matcher:
                self.set_matcher(r'.*')

            if self.topCmd.exit_code == self.topCmd.codeDone:
                pass    # continue execute the cmd list
            elif self.topCmd.exit_code == self.topCmd.codeExit:
                break

        if os.path.exists(f'{self.alive}'):
            os.remove(f'{self.alive}')

        self.que.put(EventExit())
        print("BYE")


    def prepare_run_cmdlist(self):
        self.cmd_list.extend(self.topCmd.cmd_list)
        self.topCmd.cmd_list.clear()
        self.trans_state(StateCmd(self, self), self.cmd_list)
        #self.que.put('TriggerOutfilter')
        self.child.sendline('')    # trigger output_filter


    def input_filter(self, s):
        #global proc, bash_prompt, input_buf, filter_buf_size, let_me_out

        ##input_buf += s
        ##if input_buf[0] == b'@':
        ##    MyInterpreter().cmdloop()
        return s


    def output_active_match(self):
        if not self.filter_matcher:
            return False
        res = self.filter_matcher.match(self.outfilter_buf)
        if res:
            self.filter_matcher = None
            line = self.outfilter_buf
            self.outfilter_buf = ''
            self.logger.log(DEBUG, f'"{self.state.name}": {line}')
            self.state.parse_line(line, self.next_cmds)
            return True
        return False


    # drive by line-base
    def output_filter(self, s):
        if not self.state.is_filter():
            return s

        self.outfilter_buf += s.decode('utf-8')

        # debug
        if self.filter_matcher:
            self.logger.log(DETAIL, f'wilson State-{self.state.name}: {self.outfilter_buf}')

        if "\n" in self.outfilter_buf:
            lines = self.outfilter_buf.split("\n")
            if not lines:
                return s
            #self.logger.log(DEBUG, f'{lines}')
            if self.outfilter_buf.endswith("\n"):
                self.outfilter_buf = ''
            else:
                self.outfilter_buf = lines[-1]
                lines = lines[:-1]

            for line in lines:
                line = line.strip('\r')
                self.logger.log(TRACE, f'State-{self.state.name}: {line}')
                if not self.state.parse_line(line, self.next_cmds):
                    break

        if self.outfilter_buf:
            self.output_active_match()

        while self.next_cmds:
            self.child.sendline(self.next_cmds.pop(0))

        return s



if __name__ == '__main__':
    # main()
    import doctest
    doctest.testmod()

def in_doctest():
    return hasattr(sys.modules['__main__'], '_SpoofOut')

if in_doctest():
    me = Interact(None)
