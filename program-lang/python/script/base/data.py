class EventAbs:

    def __init__(self, name):
        self.name = name


class EventDelay(EventAbs):

    def __init__(self, seconds, cmdstr):
        super().__init__('delay')
        self.seconds = seconds
        self.cmdstr = cmdstr


class EventExit(EventAbs):

    def __init__(self):
        super().__init__('exit')

