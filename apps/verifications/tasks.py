from celery import Celery
import sys
import logging
# sys.path.append('/home/ubuntu/eth_control/libs')
sys.path.append('/home/python/eth_control/libs')

from aliyunsms import send_sms

# brokers = 'redis://192.168.1.43:6379/13'
# backend = 'redis://192.168.1.43:6379/14'
brokers = 'redis://127.0.0.1:6379/13'
backend = 'redis://127.0.0.1:6379/14'

celery_app = Celery('tasks', broker=brokers, backend=backend)

logger = logging.getLogger("django")


@celery_app.task
def send_sms_code(mobile, code):
    """
    发送短信验证码
    :param mobile: 手机号
    :param code: 验证码
    :param expires: 有效期
    :return: None
    """
    try:
        # result = send_sms(mobile, code)
        result = b'{"Message":"OK","RequestId":"62F70A5E-F07A-47AB-B0F7-87ED31FEA8E4","BizId":"353716139245404387^0","Code":"OK"}'
    except Exception as e:
        logger.error("发送验证码短信[异常][ mobile: %s, message: %s ]" % (mobile, e))
    else:
        if result.decode().find('OK'):
            logger.info("发送验证码短信[正常][ mobile: %s ]" % mobile)
            return 'ok'
        else:
            logger.warning("发送验证码短信[失败][ mobile: %s ]" % mobile)