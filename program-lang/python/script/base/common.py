"""Common base for every class."""

import os
import logging
import logging.config
from config.logger import LOGGING_CONFIG


#from base.common import *
# <or>
#from base.common import DETAIL, TRACE, TRACE2, DEBUG, INFO, WARNING, ERROR, CRITICAL
#from base.common import tagNormal, tagKeyword, tagString, tagNumber, tagFunction

# Add log level: trace, detail
CRITICAL    = 50
ERROR       = 40
WARNING     = 30
INFO        = 20
DEBUG       = 10
TRACE       = 5
TRACE2      = 5
DETAIL      = 2
NOTSET      = 0

# Work with thirdpart colorize tool
tagNormal   = '@normal@'
tagKeyword  = '@keyword@'
tagString   = '@string@'
tagNumber   = '@number@'
tagFunction = '@function@'


class BaseCommon:
    """Common base part of all classes."""

    load_logconf = False
    info_debugfile = False

    def __init__(self, ctx, args):
        """Construct to propagate context."""
        self.ctx = ctx
        self.args = args

        if not BaseCommon.load_logconf:
            BaseCommon.load_logconf = True
            logging.config.dictConfig(LOGGING_CONFIG)
            # @todo ???: call once have no use
            #BaseCommon.args_verbose(logging.root, self.args.verbosity, self.args.logfile)

        BaseCommon.args_verbose(logging.root, self.args.verbosity, self.args.logfile)
        self.logger = logging.getLogger(type(self).__name__)
        #print(f"logger {self.logger.handlers}")
        #BaseCommon.args_verbose(self.logger, self.args.verbosity, self.args.logfile)

    def treat_the_linter(self):
        """Let the linter be happy."""

    def treat_the_linter2(self):
        """Let the linter be happy 2."""

    @staticmethod
    def add_arg_verbose(parser):
        parser.add_argument("-v", "--verbosity", action="count", default=0,
                help="increase output verbosity")
        parser.add_argument("-l", "--logfile", help="log file")

    @staticmethod
    def print(obj):
        import pprint
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(vars(obj))

        #import jsonpickle # pip3 install --user jsonpickle
        #import json
        #serialized = jsonpickle.encode(obj)
        #print(json.dumps(json.loads(serialized), indent=4))

        #import yaml # pip3 install --user pyyaml
        #erialized = pyyaml.encode(obj)
        #print(yaml.dump(yaml.load(serialized), indent=2))

    @staticmethod
    def dump_obj(obj, level=0):
        import types
        for key, value in obj.__dict__.items():
            if not isinstance(value, types.InstanceType):
                 print(" " * level + "{key} -> {value}")
            else:
                BaseCommon.dump_obj(value, level + 2)

    @staticmethod
    def tostr(obj):
        return str(obj.__class__) + ": " + str(obj.__dict__)
    vars

    @staticmethod
    def args_verbose(logger, verbosity, logfile):
        # https://docs.scrapy.org/en/latest/_modules/scrapy/utils/log.html
        # https://docs.python.org/3/howto/argparse.html
        #
        #print(f'verbosity={verbosity}')
        #logging.root.removeHandler
        # @note
        # v     set console at info-level
        # vv    set file at debug-level
        # vvv   set file at trace-level
        # vvvv  set file at detail-level
        if verbosity >= 4:
            logger.setLevel(DETAIL)
            for handler in logger.handlers:
                if isinstance(handler, logging.handlers.RotatingFileHandler):
                    if logfile:
                        handler.close()
                        handler.baseFilename = os.path.abspath(logfile)
                    if not BaseCommon.info_debugfile:
                        BaseCommon.info_debugfile = True
                        logger.info(f"Debug file '{handler.baseFilename}' ...")
                    handler.setLevel(DETAIL)
                elif isinstance(handler, logging.StreamHandler):
                    handler.setLevel(logging.INFO)
        elif verbosity >= 3:
            logger.setLevel(TRACE)
            for handler in logger.handlers:
                if isinstance(handler, logging.handlers.RotatingFileHandler):
                    if logfile:
                        handler.close()
                        handler.baseFilename = os.path.abspath(logfile)
                    if not BaseCommon.info_debugfile:
                        BaseCommon.info_debugfile = True
                        logger.info(f"Debug file '{handler.baseFilename}' ...")
                    handler.setLevel(TRACE)
                elif isinstance(handler, logging.StreamHandler):
                    handler.setLevel(logging.INFO)
        elif verbosity >= 2:
            logger.setLevel(logging.DEBUG)
            for handler in logger.handlers:
                #print(f"isinstance stream={isinstance(handler, logging.StreamHandler)}, file={isinstance(handler, logging.handlers.RotatingFileHandler)}")
                if isinstance(handler, logging.handlers.RotatingFileHandler):
                    if logfile:
                        handler.close()
                        handler.baseFilename = os.path.abspath(logfile)
                    #print(f"{BaseCommon.tostr(handler)}")
                    if not BaseCommon.info_debugfile:
                        BaseCommon.info_debugfile = True
                        logger.info(f"Debug file '{handler.baseFilename}' ...")
                    handler.setLevel(logging.DEBUG)
                elif isinstance(handler, logging.StreamHandler):
                    handler.close()
                    handler.setLevel(logging.INFO)
                    logger.removeHandler(handler)
        elif verbosity >= 1:
            logger.setLevel(logging.INFO)
            for handler in logger.handlers:
                if isinstance(handler, logging.handlers.RotatingFileHandler):
                    handler.close()
                    logger.removeHandler(handler)
                elif isinstance(handler, logging.StreamHandler):
                    handler.setLevel(logging.INFO)
        else:
            logger.setLevel(logging.WARNING)
            for handler in logger.handlers:
                if isinstance(handler, logging.handlers.RotatingFileHandler):
                    handler.close()
                    logger.removeHandler(handler)
                elif isinstance(handler, logging.StreamHandler):
                    handler.close()
                    logger.removeHandler(handler)



class Common(BaseCommon):
    """Common part of all classes with convenient constructor."""

    def __init__(self, common):
        """ctor."""
        super().__init__(common.ctx, common.args)


