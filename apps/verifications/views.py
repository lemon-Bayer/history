from django.shortcuts import render

# Create your views here.
from libs.captcha.captcha import check_aliyun_captcha
from django.http import HttpResponse
from django_redis import get_redis_connection
from rest_framework.views import APIView
import random, time
from rest_framework.response import Response
import sys
# sys.path.append('/home/ubuntu/eth_control/apps/verifications')
sys.path.append('/home/python/eth_control/apps/verifications')
import tasks
import pickle


class SliderView(APIView):
    """
    滑块验证
    """
    def get(self, request, session, sig, token, scene):
        try:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        except:
            ip = request.META['REMOTE_ADDR']
        check_aliyun_captcha(session, sig, token, scene, ip)
        return Response({'message': 'ok'})


class SMSCodeView(APIView):
    """短信验证码"""
    # serializer_class = ImageCodeCheckSerializer

    def get(self, request, mobile):
        # 获取前段的数据
        # data = request.query_params
        # # 定义序列化器对象,进行校验
        # ser = self.get_serializer(data=data)
        # ser.is_valid(raise_exception=True)

        # 检查是否在60s内有发送记录在序列化器中进行

        # 生成短信验证码
        sms_code = "%06d" % random.randint(0, 999999)
        print(sms_code)
        # 发送短信验证码
        result = tasks.send_sms_code.delay(mobile, sms_code)
        ce = get_redis_connection('tasks')
        time.sleep(0.5)
        while True:
            try:
                message = pickle.loads(ce.get('celery-task-meta-%s' % result))
                break
            except:
                print('继续取')
        if message['result'] == 'ok':
            # 返回OK
            # 保存验证码
            conn = get_redis_connection('verify_codes')
            conn = conn.pipeline()
            conn.setex('sms_%s' % mobile, 300, sms_code)
            conn.execute()
            return Response({'message': 'ok'})
        else:
            return Response({'message': 'no'})