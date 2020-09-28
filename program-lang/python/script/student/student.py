import getpass
import pysvn

from base.common import Common

class Student(Common):

    def __init__(self, common):
        """ctor."""
        super().__init__(common)

    def getSvnClient():
        password = self.args.svn_password
        if not password:
            password = getpass.getpass(f'Enter SVN password for user "{self.args.svn_username}": ')

        client = pysvn.Client()
        client.callback_get_login = lambda realm, username, may_save: (True, self.args.svn_username, password, True)
        return client

    def run(self):
        self.logger.info("wilson test1")
        self.logger.debug("wilson test2")
