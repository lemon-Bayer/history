# coding: utf-8
from aliyunsdkcore import client
from .aliyunsdkafs.request.v20180112 import AuthenticateSigRequest
from aliyunsdkcore.profile import region_provider
region_provider.add_endpoint('afs', 'cn-hangzhou', 'afs.aliyuncs.com')
AccessKeyId = 'LTAI6o809CEmwzYW'
AccessKeySecret = 'ZPjATsftV9yc9kbL7kWfz1dE1TWCIe'

clt = client.AcsClient(AccessKeyId, AccessKeySecret, 'cn-hangzhou')


def check_aliyun_captcha(session, sig, token, scene, ip):
    request = AuthenticateSigRequest.AuthenticateSigRequest()
    # 必填参数：从前端获取，不可更改，android和ios只传这个参数即可
    request.set_SessionId(session)
    # 必填参数：从前端获取，不可更改
    request.set_Sig(sig)
    # 必填参数：从前端获取，不可更改
    request.set_Token(token)
    # 必填参数：从前端获取，不可更改
    request.set_Scene(scene)
    # 必填参数：后端填写
    request.set_AppKey('FFFF0N00000000006E27')
    # 必填参数：后端填写
    request.set_RemoteIp(ip)
    result = clt.do_action(request)  # 返回code 100表示验签通过，900表示验签失败


