# _*_ coding:utf-8_*_


class CommonError(object):
    '''
    公用错误码, 为以后单独提出来作准备
    定义0-1000的错误码
    '''
    SUCCESS = 0
    ERROR_COMMON_REQUEST_PARAM_INVALID = 1
    ERROR_COMMON_ACCESS_DENIED = 2
    ERROR_COMMON_PARSE_JSON_FAILED = 3
    ERROR_COMMON_ILLEGAL_CHARACTER = 4
    ERROR_COMMON_NOT_LOGIN=5
    ERROR_COMMON_PROTOCOL_FOR_INTERNAL_ONLY = 6
    ERROR_COMMON_PROTOCOL_FOR_EXTERNAL_ONLY = 7

    ERROR_COMMON_CMD_NOT_EXISTS = 10
    ERROR_COMMON_DATABASE_EXCEPTION = 11
    ERROR_USER_NOT_EXIST = 12
    ERROR_PASSWORD_ERROR = 14
    ERROR_COMMON_NO_RECORD_EXISTS = 15
    ERROR_COMMON_NOT_ENOUGH_CANDY = 900

    ERROR_COMMON_UNKNOWN = 1000

    ERROR_ADER_ALREADY_EXIST = 101
    ERROR_APP_NOT_EXIST = 102
    ERROR_APP_VERIFY_NOT_PASS = 103
    ERROR_CHN_VERIFY_NOT_PASS = 104
    ERROR_DP_NOT_SETTING = 105
    ERROR_USERAGENT_NOT_MOBILE = 106


    common_message = {
        SUCCESS: 'success',
        ERROR_COMMON_REQUEST_PARAM_INVALID: '',
        ERROR_COMMON_ACCESS_DENIED: '权限错误',
        ERROR_COMMON_PARSE_JSON_FAILED: 'JSON解析失败',
        ERROR_COMMON_ILLEGAL_CHARACTER: '请求参数中带有非法字符',
        ERROR_COMMON_NOT_LOGIN:'用户尚未登录',
        ERROR_COMMON_PROTOCOL_FOR_INTERNAL_ONLY :'权限错误, 内部接口不提供外部访问',
        ERROR_COMMON_PROTOCOL_FOR_EXTERNAL_ONLY :'权限错误, 外部接口不提供内部访问',
        ERROR_COMMON_CMD_NOT_EXISTS: '协议不存在',
        ERROR_COMMON_DATABASE_EXCEPTION: '数据操作异常',
        ERROR_COMMON_UNKNOWN: '未知错误',

        ERROR_USER_NOT_EXIST:'用户不存在',
        ERROR_PASSWORD_ERROR:'用户名或密码错误',

        ERROR_COMMON_NO_RECORD_EXISTS: '记录不存在',
        ERROR_ADER_ALREADY_EXIST: '广告主已经存在',
        ERROR_APP_NOT_EXIST: 'APP不存在',
        ERROR_APP_VERIFY_NOT_PASS: 'APP未通过审核',
        ERROR_CHN_VERIFY_NOT_PASS: '下游账号未通过审核',
        ERROR_DP_NOT_SETTING: '扣量未设置',
        ERROR_USERAGENT_NOT_MOBILE: '不是移动端访问'
}

class BaseError(CommonError):
    '''
    本模块从11001-11999
    为了防止错误码重复, 按人分配区域
    cj: 1-200
    shenhong: 200-400
    yuheng: 400-600
    yuanyuan: 600-800
    chenliang: 800-999
    '''


    # code

    ERROR_RONG_REQUEST_ERROR=11201

    message = {
        ERROR_RONG_REQUEST_ERROR:'融云请求错误'
    }

    message.update(CommonError.common_message)


    @staticmethod
    def get_message(code):
        return BaseError.message.get(code)
