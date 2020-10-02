import os
import re
import cmd2
import pexpect

from base.common import Common
from cmdssh.log.show import MyInterpreter

class Interact(Common):

    def __init__(self, common):
        """ctor."""
        super().__init__(common)


    def run(self):
        self.logger.info("wilson test1")

        filter_buf = ''
        input_buf = ''
        filter_buf_size = 256
        let_me_out = False
        bash_prompt = re.compile('bash-[.0-9]+[$#] $')

        proc = pexpect.spawn('bash --noprofile --norc')
        #proc = pexpect.spawn('bash --noprofile --norc')

        while True:
            proc.interact(input_filter=self.input_filter, output_filter=self.output_filter)
            cmd1 = MyInterpreter()
            cmd1.try_parse_cmd("hello")
            cmd1.try_parse_cmd("level1")
            cmd1.cmdloop()

        print("BYE")



    def input_filter(self, s):
        #global proc, bash_prompt, input_buf, filter_buf_size, let_me_out

        ##input_buf += s
        ##if input_buf[0] == b'@':
        ##    MyInterpreter().cmdloop()
        return s


    def output_filter(self, s):
        #global proc, bash_prompt, filter_buf, filter_buf_size, let_me_out

        #filter_buf += s.decode('utf-8')
        #filter_buf = filter_buf[-filter_buf_size:]

        #if "LET ME OUT" in filter_buf:
        #    let_me_out = True

        #if bash_prompt.search(filter_buf):
        #    if let_me_out:
        #        proc.sendline('exit')
        #        proc.expect(pexpect.EOF)
        #        proc.wait()
        #    #else:
        #    #    proc.sendline('python')

        return s


