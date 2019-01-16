from rest_framework import serializers
import re
from django_redis import get_redis_connection


class CreateUserSerializer(serializers.Serializer):
    """
    创建用户序列化器
    """
    sms_code = serializers.CharField(label='短信验证码', write_only=True)
    mobile = serializers.CharField(label='手机号', write_only=True)
    invite_num_son = serializers.CharField(write_only=True)
    username = serializers.CharField(label='用户名', write_only=True)
    purse_addr = serializers.CharField(label='钱包地址', write_only=True)

    def validate_purse_addr(self, value):
        """校验钱包地址"""
        if not re.match(r'^0x[a-zA-Z0-9]{40}$', value):
            raise serializers.ValidationError('钱包地址格式错误')
        return value

    def validate_mobile(self, value):
        """验证手机号"""
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号格式错误')
        return value

    def validate_invite_num_son(self, value):
        """验证手机号"""
        if not re.match(r'\d{5}$', value):
            raise serializers.ValidationError('邀请码格式错误')
        return value

    def validate(self, attrs):
        # 判断短信验证码
        redis_conn = get_redis_connection('verify_codes')
        mobile = attrs['mobile']
        real_sms_code = redis_conn.get('sms_%s' % mobile)

        if real_sms_code is None:
            raise serializers.ValidationError('短信验证码过期!')

        if attrs['sms_code'] != real_sms_code.decode():
            raise serializers.ValidationError('短信验证码错误!')

        return attrs


class AuthenticationUser(serializers.Serializer):
    """
    登录序列化器
    """
    sms_code = serializers.CharField(label='短信验证码', write_only=True)
    mobile = serializers.CharField(label='手机号', write_only=True)

    def validate_mobile(self, value):
        """验证手机号"""
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号格式错误')
        return value

    def validate(self, attrs):
        mobile = attrs['mobile']
        sms_code = attrs['sms_code']
        # 判断短信验证码
        redis_conn = get_redis_connection('verify_codes')
        mobile = mobile
        real_sms_code = redis_conn.get('sms_%s' % mobile)

        if real_sms_code is None:
            raise serializers.ValidationError('短信验证码过期!')

        if sms_code != real_sms_code.decode():
            raise serializers.ValidationError('短信验证码错误!')
        del attrs['sms_code']
        return attrs