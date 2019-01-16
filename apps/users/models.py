from django.db import models
# Create your models here.
from django.utils import timezone


class User(models.Model):
    """用户模型"""
    username = models.CharField(max_length=150, unique=True, verbose_name='用户名')
    mobile = models.CharField(max_length=11, verbose_name='手机号')
    invite_num = models.CharField(max_length=5, null=True, blank=True, verbose_name='邀请码')
    invite_num_son = models.CharField(max_length=5, null=True, blank=True, verbose_name='邀请码')
    eth = models.CharField(max_length=20, default=0, verbose_name='投资数量')
    purse_addr = models.CharField(max_length=42, unique=True, verbose_name='钱包地址')
    is_staff = models.BooleanField(default=False, verbose_name='权限')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = 'users'


class Information(models.Model):
    username = models.CharField(max_length=150, unique=True, verbose_name='用户名')
    mobile = models.CharField(max_length=11, verbose_name='手机号')
    investment_eth = models.CharField(max_length=20, default=0, verbose_name='投资数量')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        db_table = 'vm_information'


class Bonus(models.Model):
    username = models.CharField(max_length=150, unique=True, verbose_name='用户名')
    mobile = models.CharField(max_length=11, verbose_name='手机号')
    bonus = models.CharField(max_length=11, default=0, verbose_name='奖金')
    is_active = models.BooleanField(default=False, verbose_name='状态')
    release_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        db_table = 'bonus'


