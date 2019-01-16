from rest_framework import serializers
from django_redis import get_redis_connection
from libs.captcha.captcha import check_aliyun_captcha


class ImageCodeCheckSerializer(serializers.Serializer):
    """滑块序列化器校验"""
    image_code_id = serializers.UUIDField()
    text = serializers.CharField(max_length=4, min_length=4, label="图片验证码")

    def validate(self, attrs):
        """
        校验
        """
        image_code_id = attrs['image_code_id']
        text = attrs['text']
        # 连接redis 查询图片验证码
        conn = get_redis_connection('verify_codes')
        real_image_code = conn.get('img_%s' % image_code_id)
        if not real_image_code:
            raise serializers.ValidationError('图片验证码失效!')

        # 删除图片验证码
        conn.delete('img_%s' % image_code_id)

        # 校验图片验证码
        if text.lower() != real_image_code.decode().lower():
            raise serializers.ValidationError('图片验证码错误!')

        # 判断是否在60s内
        mobile = self.context['view'].kwargs['mobile']
        send_flag = conn.get('send_flag%s' % mobile)
        if send_flag:
            raise serializers.ValidationError('请求次数过于频繁!')

        return attrs


class SliderSerializer(serializers.Serializer):
    session = serializers.CharField()
    token = serializers.CharField()
    sig = serializers.CharField()
    scene = serializers.CharField()

    def validate(self, attrs):
        session = attrs['session']
        print(session)
        sig = attrs['sig']
        print(sig)
        token = attrs['token']
        print(token)
        scene = attrs['scene']
        print(scene)
        check_aliyun_captcha(session, sig, token, scene)
        print(attrs)
        return