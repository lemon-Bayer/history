# -*- coding: utf-8 -*-
import json
import sys, importlib
from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from aliyunsdkdysmsapi.request.v20170525 import QuerySendDetailsRequest
from aliyunsdkcore.client import AcsClient
import uuid
from aliyunsdkcore.profile import region_provider
from aliyunsdkcore.http import method_type as MT
from aliyunsdkcore.http import format_type as FT

"""
短信业务调用接口示例，版本号：v20170525
Created on 2017-06-12
"""
try:
    importlib.reload(sys)
except NameError:
    pass
except Exception as err:
    raise err

ACCESS_KEY_ID = "LTAI6o809CEmwzYW"
ACCESS_KEY_SECRET = "ZPjATsftV9yc9kbL7kWfz1dE1TWCIe"

# 注意：不要更改
REGION = "cn-hangzhou"
PRODUCT_NAME = "Dysmsapi"
DOMAIN = "dysmsapi.aliyuncs.com"
acs_client = AcsClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET, REGION)
region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)


# def send_sms(business_id, phone_numbers, sign_name, template_code, template_param=None):
def send_sms(phone_numbers, code):
    """
    发送短信接口，在需要使用的地方引用该模块，然后调用该接口即可
    :param phone_numbers:发送的手机号码
    :param sign_name: 应用名
    :param template_code: 模板名称
    :param template_param: 模板变量参数
    :return:
    """
    # 将部分参数固定，在调用方法的时候更简洁，因为这些参数一般不会改变
    sign_name = 'DLB会员查询系统'  # 应用名称
    template_code = 'SMS_147417206'  # 模板名称
    template_param = json.dumps({'code': code})  # 模板变量参数

    business_id = uuid.uuid1()
    smsRequest = SendSmsRequest.SendSmsRequest()
    # 申请的短信模板编码,必填
    smsRequest.set_TemplateCode(template_code)

    # 短信模板变量参数
    if template_param is not None:
        smsRequest.set_TemplateParam(template_param)
    # 设置业务请求流水号，必填。
    smsRequest.set_OutId(business_id)
    # 短信签名
    smsRequest.set_SignName(sign_name)
    # 数据提交方式
    # smsRequest.set_method(MT.POST)
    # 数据提交格式
    # smsRequest.set_accept_format(FT.JSON)
    # 短信发送的号码列表，必填。
    smsRequest.set_PhoneNumbers(phone_numbers)
    # 调用短信发送接口，返回json
    smsResponse = acs_client.do_action_with_exception(smsRequest)
    # TODO 业务处理
    print(smsResponse)
    return smsResponse

# 这是测试用的代码
# if __name__ == '__main__':
#     __business_id = uuid.uuid1()
#     # print(__business_id)
#     # ,\"product\":\"云通信\"}"
#     params = "{\"code\":\"314655\"}"
#     # params = u'{"name":"wqb","code":"12345678","address":"bz","phone":"13000000000"}'
#     print(send_sms(__business_id, "13203160137", "李靖轩", "SMS_141905211", params))
