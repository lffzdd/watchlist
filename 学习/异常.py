# raise ValueError('抛出内置异常ValueError')


class CustomError(Exception):
    """抛出自定义异常"""
    pass


# raise CustomError('Custom error message.')


class CustomError_(Exception):
    """抛出自定义异常并传递参数"""

    def __init__(self, arg):
        self.arg = arg


raise CustomError_('Custom error message with args')
