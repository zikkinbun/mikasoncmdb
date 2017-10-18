# _*_ coding:utf-8_*_
from error import BaseError

class BaseException(Exception):
    '''
    异常类
    '''
    def __init__(self, code, **kwargs):
        '''
        Constructor
        '''
        self.code = code
        self.message = BaseError.get_message(code)
        self.ext = kwargs

class ParamException(BaseException):
    '''
    UFOException的一个特例
    '''

    def __init__(self, name, **kwargs):
        '''
        '''

        BaseException.__init__(self, BaseError.ERROR_COMMON_REQUEST_PARAM_INVALID, **kwargs)

        self.message = '参数缺失或非法:' + name
