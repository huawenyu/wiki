"""Common base for every class."""

import logging
from config.logger import LOGGING_CONFIG


class BaseCommon:
    """Common base part of all classes."""

    load_logconf = False
    info_debugfile = False

    def __init__(self, ctx, args):
        """Construct to propagate context."""
        self.ctx = ctx
        self.args = args
        self.args.verbosity = verbosity

        if not BaseCommon.load_logconf:
            BaseCommon.load_logconf = True
            logging.config.dictConfig(LOGGING_CONFIG)
            # @todo ???: call once have no use
            #BaseCommon.args_verbose(logging.root, self.args.verbosity)

        BaseCommon.args_verbose(logging.root, self.args.verbosity)
        self.logger = logging.getLogger(type(self).__name__)
        #print(f"logger {self.logger.handlers}")
        #BaseCommon.args_verbose(self.logger, self.args.verbosity)

    def treat_the_linter(self):
        """Let the linter be happy."""

    def treat_the_linter2(self):
        """Let the linter be happy 2."""

    @staticmethod
    def add_arg_verbose(parser):
        parser.add_argument("-v", "--verbosity", action="count", default=0,
                help="increase output verbosity")

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
    def args_verbose(logger, verbosity):
        # https://docs.scrapy.org/en/latest/_modules/scrapy/utils/log.html
        # https://docs.python.org/3/howto/argparse.html
        #
        #print(f'verbosity={self.args.verbosity}')
        #logging.root.removeHandler
        if self.args.verbosity >= 3:
            logger.setLevel(logging.DEBUG)
            for handler in logger.handlers:
                if isinstance(handler, logging.handlers.RotatingFileHandler):
                    if not BaseCommon.info_debugfile:
                        BaseCommon.info_debugfile = True
                        logger.info(f"Debug file '{handler.baseFilename}' ...")
                    handler.setLevel(logging.DEBUG)
                elif isinstance(handler, logging.StreamHandler):
                    handler.setLevel(logging.DEBUG)
        elif self.args.verbosity >= 2:
            logger.setLevel(logging.DEBUG)
            for handler in logger.handlers:
                #print(f"isinstance stream={isinstance(handler, logging.StreamHandler)}, file={isinstance(handler, logging.handlers.RotatingFileHandler)}")
                if isinstance(handler, logging.handlers.RotatingFileHandler):
                    #print(f"{BaseCommon.tostr(handler)}")
                    if not BaseCommon.info_debugfile:
                        BaseCommon.info_debugfile = True
                        logger.info(f"Debug file '{handler.baseFilename}' ...")
                    handler.setLevel(logging.DEBUG)
                elif isinstance(handler, logging.StreamHandler):
                    handler.setLevel(logging.INFO)
        elif self.args.verbosity >= 1:
            logger.setLevel(logging.INFO)
            for handler in logger.handlers:
                if isinstance(handler, logging.handlers.RotatingFileHandler):
                    handler.close()
                    logger.removeHandler(handler)
                elif isinstance(handler, logging.StreamHandler):
                    handler.setLevel(logging.INFO)
        else:
            logger.setLevel(logging.INFO)
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


