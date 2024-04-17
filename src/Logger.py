from .MultiLangLogger.python import Logger as MultiLangLogger

class Logger(MultiLangLogger):

    def __init__(self):
        super().__init__('CP Merger')


logger = Logger()