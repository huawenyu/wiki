# Requirement

	https://pysvn.sourceforge.io/downloads.html

	$ sudo apt-get install python3-apt
	$ sudo apt-get install -y python3-pysvn

# Sample svn-server:

	$ svn ls https://svn.alfresco.com/repos/alfresco-open-mirror/integrations/GoogleDocs/HEAD/Google\ Docs\ Share/src/test/resources/alfresco/web-extensio

# Module: cmd

https://pymotw.com/2/cmd/

## Parse arg ourself

https://cmd2.readthedocs.io/en/latest/features/argument_processing.html
https://github.com/python-cmd2/cmd2/blob/master/examples/example.py#L24

```python
import cmd
import urlparse

class myCmd(cmd.Cmd):
    def onecmd(self, line):
        """Mostly ripped from Python's cmd.py"""
        cmd, arg, line = self.parseline(line)
        arg = urlparse.parse_qs(arg) # <- added line
        if not line:
            return self.emptyline()
        if cmd is None:
            return self.default(line)
        self.lastcmd = line
        if cmd == '':
            return self.default(line)
        else:
            try:
                func = getattr(self, 'do_' + cmd)
            except AttributeError:
                return self.default(line)
            return func(arg)

    def do_foo(self, arg)
        print arg

my_cmd = myCmd()
my_cmd.cmdloop()
```

## group cmd, enable/disable them

https://cmd2.readthedocs.io/en/latest/features/help.html#categorizing-commands
https://cmd2.readthedocs.io/en/latest/features/disable_commands.html

# script: cmdssh.py


