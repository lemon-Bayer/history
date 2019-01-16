from django.shortcuts import render
# Create your views here.
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.views import APIView
from .models import User, Information, Bonus
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from . import serializers
from .constants import rate
from .utils import perform_authentication
from rest_framework_jwt.settings import api_settings
from datetime import datetime, timedelta
from random import randint


class UsernameCountView(APIView):
    """
    用户名数量
    """
    def get(self, request, username):
        """
        获取指定的用户名
        """
        count = User.objects.filter(username=username).count()

        data = {
            'username': username,
            'count': count
        }

        return Response(data)


class MobileCountView(APIView):
    """
    校验手机号是否注册
    """
    def get(self, request, mobile):
        """
        获取指定手机的号
        """
        count = User.objects.filter(mobile=mobile).count()

        data = {
            'mobile': mobile,
            'count': count
        }

        return Response(data)


class InviteNumCountView(APIView):
    """
    邀请码数量
    """
    def get(self, request, invite_num_son):
        """
        获取指定的邀请码
        """
        count = User.objects.filter(invite_num=invite_num_son).count()

        data = {
            'invite_num': invite_num_son,
            'count': count
        }

        return Response(data)


class PurseAddrCountView(APIView):
    """
    校验钱包地址
    """
    def get(self, request, purse_addr):
        """
        获取指定钱包数量
        """
        count = User.objects.filter(purse_addr=purse_addr).count()

        data = {
            'purse_addr': purse_addr,
            'count': count
        }

        return Response(data)


class UserView(APIView):
    """
    用户注册
    传入参数:
    mobile, image_code, sms_code, invite_num, purse_addr, allow
    """
    def post(self, request):
        ser = serializers.CreateUserSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        # 移除数据库模型类中不存在的属性
        del ser.validated_data['sms_code']
        try:
            user = User.objects.create(**ser.validated_data)
            num = "%05d" % randint(0, 99999)
            user.invite_num = num
            user.save()
            # 补充生成记录登录状态的token
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            # 为后面取user做铺垫
            conn = get_redis_connection('session')
            conn = conn.pipeline()
            conn.setex('username_%s' % token, 1800, user.username)
            conn.setex('token_%s' % token, 1800, token)
            conn.execute()
        except User.DoesNotExist:
            return Response({'message': '用户不存在'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            data = {
                'username': user.username,
                'token': token,
                'is_staff': user.is_staff,
                'level': '粉丝'
            }
            return Response(data)


class UserAuthentication(APIView):
    """
    用户登录
    传入参数：
    mobile, sms_code
    """
    def post(self, request):
        ser = serializers.AuthenticationUser(data=request.data)
        ser.is_valid(raise_exception=True)
        mobile = ser.validated_data.get('mobile')
        try:
            user = User.objects.get(mobile=mobile)
            # 补充生成记录登录状态的token
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            conn = get_redis_connection('session')
            conn = conn.pipeline()
            conn.setex('username_%s' % token, 1800, user.username)
            conn.setex('token_%s' % token, 1800, token)
            conn.execute()
        except User.DoesNotExist:
            return Response({'message': '用户不存在'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if user.eth >= 500:
                level = '城市'
            elif 100 <= user.eth < 500:
                level = '贵宾'
            elif 5 <= user.eth < 100:
                level = '会员'
            else:
                level = '粉丝'
            data = {
                'username': user.username,
                'token': token,
                'is_staff': user.is_staff,
                'level': level
            }
            return Response(data)


class UserDetailView(APIView):
    """
    用户详情
    """
    def get(self, request):
        try:
            user = perform_authentication(request)
        except Exception:
            user = None
        if user is not None and user.is_staff:
            city_num = User.objects.filter(eth__gte=500).count()
            vip_num = User.objects.filter(eth__range=[100, 499]).count()
            member_num = User.objects.filter(eth__range=[5, 99]).count()
            fans_num = User.objects.filter(eth__lt=5).count() - 1
            dt_s = datetime.now().date()
            dt_e = dt_s - timedelta(1)
            dt_t = dt_s + timedelta(1)
            yday_investment = 0
            day_investment = 0
            yday_send_bonus = 0
            day_send_bonus = 0
            investment_all = 0
            bonus_all = 0
            yday_investment_list = Information.objects.filter(create_time__range=[dt_e, dt_s])
            for im in yday_investment_list:
                yday_investment += float(im.investment_eth)
            yday_investment = '%.3f' % yday_investment
            day_investment_list = Information.objects.filter(create_time__range=[dt_s, dt_t])
            for im in day_investment_list:
                day_investment += float(im.investment_eth)
            day_investment = '%.3f' % day_investment
            yday_send_bonus_list = Bonus.objects.filter(release_time__range=[dt_e, dt_s], is_active=1)
            for im in yday_send_bonus_list:
                yday_send_bonus += float(im.bonus)
            yday_send_bonus = '%.3f' % yday_send_bonus
            day_send_bonus_list = Bonus.objects.filter(release_time__range=[dt_s, dt_t], is_active=1)
            for im in day_send_bonus_list:
                day_send_bonus += float(im.bonus)
            day_send_bonus = '%.3f' % day_send_bonus
            investment_all_list = Information.objects.all()
            for im in investment_all_list:
                investment_all += float(im.investment_eth)
            investment_all = '%.3f' % investment_all
            bonus_all_list = Bonus.objects.all()
            for im in bonus_all_list:
                if im.is_active:
                    bonus_all += float(im.bonus)
            bonus_all = '%.3f' % bonus_all
            data = {
                'city_num': city_num,
                'vip_num': vip_num,
                'member_num': member_num,
                'fans_num': fans_num,
                'yday_investment': yday_investment,
                'day_investment': day_investment,
                'yday_send_bonus': yday_send_bonus,
                'day_send_bonus': day_send_bonus,
                'bonus_all': bonus_all,
                'investment_all': investment_all
            }
            return Response(data)
        else:
            return Response({'msg': 'token失效'})


class MemberDetailView(APIView):
    """
    会员列表
    """
    def get(self, request):
        page = int(request.META.get('QUERY_STRING')[12])
        limit = int(request.META.get('QUERY_STRING')[26:28])
        try:
            user = perform_authentication(request)
        except Exception:
            user = None
        if user is not None and user.is_staff:
            user_list = User.objects.all()[(page-1)*10:page*limit]
            count = User.objects.all().count() - 1
            information = []
            # dt_s = datetime.now().date()
            # dt_t = dt_s + timedelta(1)
            for un in user_list:
                username = un.username
                if username == 'admin':
                    continue
                mobile = un.mobile
                num = un.invite_num
                eth = un.eth
                dlb = '%.3f' % (eth * rate)
                bonus = 0.0
                try:
                    bonus_user_list = Bonus.objects.filter(username=username)
                except Exception:
                    return Response({"code": 0, "msg": "", "count": 0, "data": []})
                for bn in bonus_user_list:
                    if bn.is_active:
                        bonus += float(bn.bonus)
                f_str = str(bonus)
                a, b, c = f_str.partition('.')
                c = (c + "0" * 3)[:3]
                bonus = ".".join([a, c])
                invite_num = User.objects.filter(invite_num_son=num).count()
                if eth >= 500:
                    level = '城市'
                elif 100 <= eth < 500:
                    level = 'VIP'
                elif 5 <= eth < 100:
                    level = '会员'
                else:
                    level = '粉丝'
                user_dict = {
                    'username': username,
                    'mobile': mobile,
                    'level': level,
                    'invite_num': invite_num,
                    'eth': eth,
                    'dlb': dlb,
                    'bonus': bonus
                }
                information.append(user_dict)
            # information = information[(page-1)*10:page*limit]
            data = {"code": 0, "msg": "", "count": count, "data": information}
            return Response(data)
        else:
            return Response({"code": 0, "msg": "token失效", "count": 0, "data": []})


class ExportView(APIView):
    def get(self, request):
        try:
            user = perform_authentication(request)
        except Exception:
            user = None
        if user is not None and user.is_staff:
            user_list = User.objects.all()
            information = []
            # dt_s = datetime.now().date()
            # dt_t = dt_s + timedelta(1)
            for un in user_list:
                username = un.username
                if username == 'admin':
                    continue
                mobile = un.mobile
                num = un.invite_num
                eth = un.eth
                dlb = '%.3f' % (eth * rate)
                bonus = 0.0
                try:
                    bonus_user_list = Bonus.objects.filter(username=username)
                except Exception:
                    return Response({"code": 0, "msg": "", "count": 0, "data": []})
                for bn in bonus_user_list:
                    if bn.is_active:
                        bonus += float(bn.bonus)
                f_str = str(bonus)
                a, b, c = f_str.partition('.')
                c = (c + "0" * 3)[:3]
                bonus = ".".join([a, c])
                invite_num = User.objects.filter(invite_num_son=num).count()
                if eth >= 500:
                    level = '城市'
                elif 100 <= eth < 500:
                    level = 'VIP'
                elif 5 <= eth < 100:
                    level = '会员'
                else:
                    level = '粉丝'
                user_dict = {
                    'username': username,
                    'mobile': mobile,
                    'level': level,
                    'invite_num': invite_num,
                    'eth': eth,
                    'dlb': dlb,
                    'bonus': bonus
                }
                information.append(user_dict)
            data = {"code": 200, "data": information}
            return Response(data)
        else:
            return Response({"code": 0, "data": []})


class SearchUserView(APIView):
    """
    搜索
    """
    def post(self, request):
        search = request.data.get('keyWord')
        str_type = request.data.get('keyType')
        limit = request.data.get('limit')
        page = request.data.get('page')
        try:
            user = perform_authentication(request)
        except Exception:
            user = None
        if user is not None and user.is_staff:
            try:
                if str_type == 'mobile':
                    user = User.objects.get(mobile=search)
                    username = user.username
                    mobile = user.mobile
                    num = user.invite_num
                    eth = user.eth
                    bonus = 0.0
                    try:
                        bonus_user_list = Bonus.objects.filter(username=username)
                    except Exception:
                        return Response({"code": 0, "msg": "", "count": 0, "data": []})
                    for bn in bonus_user_list:
                        if bn.is_active:
                            bonus += float(bn.bonus)
                    dlb = '%.3f' % (eth * rate)
                    f_str = str(bonus)
                    a, b, c = f_str.partition('.')
                    c = (c + "0" * 3)[:3]
                    bonus = ".".join([a, c])
                    invite_num = User.objects.filter(invite_num_son=num).count()
                    if eth >= 500:
                        level = '城市'
                    elif 100 <= eth < 500:
                        level = 'VIP'
                    elif 5 <= eth < 100:
                        level = '会员'
                    else:
                        level = '粉丝'
                    user_dict = {
                        'username': username,
                        'mobile': mobile,
                        'level': level,
                        'invite_num': invite_num,
                        'eth': eth,
                        'dlb': dlb,
                        'bonus': bonus
                    }
                    data = {"code": 0, "msg": "", "count": 1, "data": [user_dict]}
                    return Response(data)
                elif str_type == 'level':
                    if search == '城市':
                        user_list = User.objects.filter(eth__gte=500)[(page - 1) * 10:page * limit]
                        count = User.objects.filter(eth__gte=500)
                    elif search.lower() == 'vip':
                        user_list = User.objects.filter(eth__range=[100, 499])[(page - 1) * 10:page * limit]
                        count = User.objects.filter(eth__range=[100, 499])
                    elif search == '会员':
                        user_list = User.objects.filter(eth__range=[5, 99])[(page - 1) * 10:page * limit]
                        count = User.objects.filter(eth__range=[5, 99])
                    elif search == '粉丝':
                        user_list = User.objects.filter(eth__lt=5)[(page - 1) * 10:page * limit]
                        count = User.objects.filter(eth__lt=5) - 1
                    else:
                        return Response({"code": 0, "msg": "", "count": 0, "data": []})
                    # if search == '粉丝':
                    #     count = user_list.count() - 1
                    # else:
                    #     count = user_list.count()
                    information = []
                    for un in user_list:
                        username = un.username
                        if username == 'admin':
                            continue
                        mobile = un.mobile
                        num = un.invite_num
                        eth = un.eth
                        bonus = 0.0
                        try:
                            bonus_user_list = Bonus.objects.filter(username=username)
                        except Exception:
                            return Response({"code": 0, "msg": "", "count": 0, "data": []})
                        for bn in bonus_user_list:
                            if bn.is_active:
                                bonus += float(bn.bonus)
                        dlb = '%.3f' % (eth * rate)
                        f_str = str(bonus)
                        a, b, c = f_str.partition('.')
                        c = (c + "0" * 3)[:3]
                        bonus = ".".join([a, c])
                        invite_num = User.objects.filter(invite_num_son=num).count()
                        if eth >= 500:
                            level = '城市'
                        elif 100 <= eth < 500:
                            level = 'VIP'
                        elif 5 <= eth < 100:
                            level = '会员'
                        else:
                            level = '粉丝'
                        user_dict = {
                            'username': username,
                            'mobile': mobile,
                            'level': level,
                            'invite_num': invite_num,
                            'eth': eth,
                            'dlb': dlb,
                            'bonus': bonus
                        }
                        information.append(user_dict)
                    # information = information[(page - 1) * 10:page * limit]
                    data = {"code": 0, "msg": "", "count": count, "data": information}
                    return Response(data)
                elif str_type == 'username':
                    user = User.objects.get(username=search)
                    username = search
                    mobile = user.mobile
                    num = user.invite_num
                    eth = user.eth
                    bonus = 0.0
                    try:
                        bonus_user_list = Bonus.objects.filter(username=username)
                    except Exception:
                        return Response({"code": 0, "msg": "", "count": 0, "data": []})
                    for bn in bonus_user_list:
                        if bn.is_active:
                            bonus += float(bn.bonus)
                    dlb = '%.3f' % (eth * rate)
                    f_str = str(bonus)
                    a, b, c = f_str.partition('.')
                    c = (c + "0" * 3)[:3]
                    bonus = ".".join([a, c])
                    invite_num = User.objects.filter(invite_num_son=num).count()
                    if eth >= 500:
                        level = '城市'
                    elif 100 <= eth < 500:
                        level = 'VIP'
                    elif 5 <= eth < 100:
                        level = '会员'
                    else:
                        level = '粉丝'
                    user_dict = {
                        'username': username,
                        'mobile': mobile,
                        'level': level,
                        'invite_num': invite_num,
                        'eth': eth,
                        'dlb': dlb,
                        'bonus': bonus
                    }
                    data = {"code": 0, "msg": "", "count": 1, "data": [user_dict]}
                    return Response(data)
                else:
                    return Response({"code": 0, "msg": "", "count": 0, "data": []})
            except Exception:
                return Response({"code": 0, "msg": "", "count": 0, "data": []})
        else:
            return Response({"code": 0, "msg": "token失效", "count": 0, "data": []})


class GrantUserView(APIView):
    """
    投资信息
    """
    def get(self, request):
        page = int(request.META.get('QUERY_STRING')[12])
        limit = int(request.META.get('QUERY_STRING')[26:28])
        try:
            user = perform_authentication(request)
        except Exception:
            user = None
        if user is not None and user.is_staff:
            user_list = Bonus.objects.all()[(page - 1) * 10:page * limit]
            count = Bonus.objects.all().count()
            # dt_s = datetime.now().date()
            # dt_t = dt_s + timedelta(1)
            information = []
            for un in user_list:
                day_time = str(un.release_time)
                username = un.username
                bonus = un.bonus
                mobile = un.mobile
                is_active = un.is_active
                if is_active:
                    state = '已发放'
                else:
                    state = '未发放'
                user_dict = {
                    'day_time': day_time,
                    'username': username,
                    'mobile': mobile,
                    'bonus': bonus,
                    'is_active': state
                }
                information.append(user_dict)
            # information = information[(page - 1) * 10:page * limit]
            data = {"code": 0, "msg": "", "count": count, "data": information}
            return Response(data)
        else:
            return Response({"code": 0, "msg": "token失效", "count": 0, "data": []})


class GrantSearchView(APIView):
    """
    投资搜索
    """
    def post(self, request):
        search = request.data.get('keyWord')
        str_type = request.data.get('keyType')
        page = request.data.get('page')
        limit = request.data.get('limit')
        try:
            if str_type == 'day_time':
                # 转时间戳
                # dt_s = time.mktime(time.strptime(search, '%Y-%m-%d %H:%M:%S'))
                # dt_s = datetime.fromtimestamp(dt_s)
                # dt_s = datetime.strptime(search, '%Y-%m-%d %H:%M:%S')
                user_list = Bonus.objects.filter(release_time__contains=search)[(page - 1) * 10:page * limit]
                count = Bonus.objects.filter(release_time__contains=search).count()
                information = []
                for un in user_list:
                    day_time = str(un.release_time)
                    username = un.username
                    bonus = un.bonus
                    mobile = un.mobile
                    is_active = un.is_active
                    if is_active:
                        state = '已发放'
                    else:
                        state = '未发放'
                    user_dict = {
                        'day_time': day_time,
                        'username': username,
                        'mobile': mobile,
                        'bonus': bonus,
                        'is_active': state
                    }
                    information.append(user_dict)
                # information = information[(page - 1) * 10:page * limit]
                data = {"code": 0, "msg": "", "count": count, "data": information}
                return Response(data)
            elif str_type == 'username':
                user_list = Bonus.objects.filter(username=search)[(page - 1) * 10:page * limit]
                count = user_list.count()
                information = []
                for un in user_list:
                    day_time = str(un.release_time)
                    username = un.username
                    bonus = un.bonus
                    mobile = un.mobile
                    is_active = un.is_active
                    if is_active:
                        state = '已发放'
                    else:
                        state = '未发放'
                    user_dict = {
                        'day_time': day_time,
                        'username': username,
                        'mobile': mobile,
                        'bonus': bonus,
                        'is_active': state
                    }
                    information.append(user_dict)
                # information = information[(page - 1) * 10:page * limit]
                data = {"code": 0, "msg": "", "count": count, "data": information}
                return Response(data)
        except Exception:
            return Response({"code": 0, "msg": "", "count": 0, "data": []})


class MemberUserView(APIView):
    """
    用户个人信息
    """
    def get(self, request):
        try:
            user = perform_authentication(request)
        except Exception:
            user = None
        if user is not None:
            username = user.username
            mobile = user.mobile
            num_code = user.invite_num
            eth = user.eth
            bonus = 0.0
            try:
                bonus_user_list = Bonus.objects.filter(mobile=mobile)
            except Exception:
                return Response({"code": 0, "msg": "", "count": 0, "data": []})
            for bn in bonus_user_list:
                if bn.is_active:
                    bonus += float(bn.bonus)
            dlb = '%.3f' % (eth * rate)
            invite_num = User.objects.filter(invite_num_son=num_code).count()
            if eth >= 500:
                level = '城市'
            elif 100 <= eth < 500:
                level = 'VIP'
            elif 5 <= eth < 100:
                level = '会员'
            else:
                level = '粉丝'
            user_dict = {
                'username': username,
                'mobile': mobile,
                'level': level,
                'invite_num': invite_num,
                'eth': eth,
                'dlb': dlb,
                'num_code': num_code,
                'bonus': bonus
            }
            data = {"code": 0, "msg": "", "count": 1, "data": [user_dict]}
            return Response(data)
        else:
            return Response({"code": 0, "msg": "token失效", "count": 0, "data": []})


class VIPNodeView(APIView):
    """
    VIP节点信息
    """
    def get(self, request):
        page = int(request.META.get('QUERY_STRING')[12])
        limit = int(request.META.get('QUERY_STRING')[26:28])
        try:
            user = perform_authentication(request)
        except Exception:
            user = None
        if user is not None:
            if user.eth >= 500:
                information = []
                num_code = user.invite_num
                user_list = User.objects.filter(invite_num_son=num_code, eth__range=[100, 499])[(page - 1) * 10:page * limit]
                count = User.objects.filter(invite_num_son=num_code, eth__range=[100, 499]).count()
                for ul in user_list:
                    username = ul.username
                    mobile = ul.mobile
                    eth = ul.eth
                    if eth >= 500:
                        level = '城市'
                    elif 100 <= eth < 500:
                        level = 'VIP'
                    elif 5 <= eth < 100:
                        level = '会员'
                    else:
                        level = '粉丝'
                    user_dict = {
                        'username': username,
                        'mobile': mobile,
                        'level': level,
                        'eth': eth
                    }
                    information.append(user_dict)
                # information = information[(page - 1) * 10:page * limit]
                data = {"code": 0, "msg": "", "count": count, "data": information}
                return Response(data)
            else:
                return Response({"code": 0, "msg": "", "count": 0, "data": []})
        else:
            return Response({"code": 0, "msg": "token失效", "count": 0, "data": []})


class MemNodeView(APIView):
    """
    会员节点信息
    """
    def get(self, request):
        page = int(request.META.get('QUERY_STRING')[12])
        limit = int(request.META.get('QUERY_STRING')[26:28])
        try:
            user = perform_authentication(request)
        except Exception:
            user = None
        if user is not None:
            if user.eth >= 100:
                information = []
                num_code = user.invite_num
                user_list = User.objects.filter(invite_num_son=num_code, eth__range=[5, 99])[(page - 1) * 10:page * limit]
                count = User.objects.filter(invite_num_son=num_code, eth__range=[5, 99]).count()
                for ul in user_list:
                    username = ul.username
                    mobile = ul.mobile
                    eth = ul.eth
                    if eth >= 500:
                        level = '城市'
                    elif 100 <= eth < 500:
                        level = 'VIP'
                    elif 5 <= eth < 100:
                        level = '会员'
                    else:
                        level = '粉丝'
                    user_dict = {
                        'username': username,
                        'mobile': mobile,
                        'level': level,
                        'eth': eth
                    }
                    information.append(user_dict)
                # information = information[(page - 1) * 10:page * limit]
                data = {"code": 0, "msg": "", "count": count, "data": information}
                return Response(data)
            else:
                return Response({"code": 0, "msg": "", "count": 0, "data": []})
        else:
            return Response({"code": 0, "msg": "token失效", "count": 0, "data": []})


class FansNodeView(APIView):
    """
    粉丝节点信息
    """
    def get(self, request):
        page = int(request.META.get('QUERY_STRING')[12])
        limit = int(request.META.get('QUERY_STRING')[26:28])
        try:
            user = perform_authentication(request)
        except Exception:
            user = None
        if user is not None:
            if user.eth >= 5:
                information = []
                num_code = user.invite_num
                user_list = User.objects.filter(invite_num_son=num_code, eth__lt=5)[(page - 1) * 10:page * limit]
                count = User.objects.filter(invite_num_son=num_code, eth__lt=5).count()
                for ul in user_list:
                    username = ul.username
                    mobile = ul.mobile
                    eth = ul.eth
                    if eth >= 500:
                        level = '城市'
                    elif 100 <= eth < 500:
                        level = 'VIP'
                    elif 5 <= eth < 100:
                        level = '会员'
                    else:
                        level = '粉丝'
                    user_dict = {
                        'username': username,
                        'mobile': mobile,
                        'level': level,
                        'eth': eth
                    }
                    information.append(user_dict)
                # information = information[(page - 1) * 10:page * limit]
                data = {"code": 0, "msg": "", "count": count, "data": information}
                return Response(data)
            else:
                return Response({"code": 0, "msg": "", "count": 0, "data": []})
        else:
            return Response({"code": 0, "msg": "token失效", "count": 0, "data": []})


class SearchNodeView(APIView):
    """
    搜索节点信息
    """
    def post(self, request):
        search = request.data.get('keyWord')
        str_type = request.data.get('keyType')
        page = request.data.get('page')
        limit = request.data.get('limit')
        level = request.data.get('level')
        try:
            user = perform_authentication(request)
        except Exception:
            return Response({"code": 0, "msg": "token失效", "count": 0, "data": []})
        invite_num = user.invite_num
        if level == 'vip':
            if str_type == 'username':
                try:
                    search_user = User.objects.get(invite_num_son=invite_num, username=search, eth__range=[100, 499])
                except:
                    return Response({"code": 0, "msg": "", "count": 0, "data": []})
                username = search_user.username
                mobile = search_user.mobile
                eth = search_user.eth
                user_dict = {
                    'username': username,
                    'mobile': mobile,
                    'level': 'VIP',
                    'eth': eth,
                }
                data = {"code": 0, "msg": "", "count": 1, "data": [user_dict]}
                return Response(data)
            elif str_type == 'level':
                if search.lower() == 'vip':
                    try:
                        user_list = User.objects.filter(invite_num_son=invite_num, eth__range=[100, 499])[(page - 1) * 10:page * limit]
                        count = User.objects.filter(invite_num_son=invite_num, eth__range=[100, 499]).count()
                    except:
                        return Response({"code": 0, "msg": "", "count": 0, "data": []})
                else:
                    return Response({"code": 0, "msg": "", "count": 0, "data": []})
                information = []
                for un in user_list:
                    username = un.username
                    mobile = un.mobile
                    eth = un.eth
                    user_dict = {
                        'username': username,
                        'mobile': mobile,
                        'level': 'VIP',
                        'eth': eth
                    }
                    information.append(user_dict)
                # information = information[(page - 1) * 10:page * limit]
                data = {"code": 0, "msg": "", "count": count, "data": information}
                return Response(data)
            else:
                return Response({"code": 0, "msg": "", "count": 0, "data": []})
        elif level == 'mem':
            if str_type == 'username':
                try:
                    search_user = User.objects.get(invite_num_son=invite_num, username=search, eth__range=[5, 99])
                except:
                    return Response({"code": 0, "msg": "", "count": 0, "data": []})
                username = search_user.username
                mobile = search_user.mobile
                eth = search_user.eth
                user_dict = {
                    'username': username,
                    'mobile': mobile,
                    'level': 'VIP',
                    'eth': eth,
                }
                data = {"code": 0, "msg": "", "count": 1, "data": [user_dict]}
                return Response(data)
            elif str_type == 'level':
                if search == '会员':
                    try:
                        user_list = User.objects.filter(invite_num_son=invite_num, eth__range=[5, 99])[(page - 1) * 10:page * limit]
                        count = User.objects.filter(invite_num_son=invite_num, eth__range=[5, 99]).count()
                    except:
                        return Response({"code": 0, "msg": "", "count": 0, "data": []})
                else:
                    return Response({"code": 0, "msg": "", "count": 0, "data": []})
                information = []
                for un in user_list:
                    username = un.username
                    mobile = un.mobile
                    eth = un.eth
                    user_dict = {
                        'username': username,
                        'mobile': mobile,
                        'level': '会员',
                        'eth': eth
                    }
                    information.append(user_dict)
                # information = information[(page - 1) * 10:page * limit]
                data = {"code": 0, "msg": "", "count": count, "data": information}
                return Response(data)
        elif level == 'fans':
            if str_type == 'username':
                try:
                    search_user = User.objects.get(invite_num_son=invite_num, username=search, eth__lt=5)
                except:
                    return Response({"code": 0, "msg": "", "count": 0, "data": []})
                username = search_user.username
                mobile = search_user.mobile
                eth = search_user.eth
                user_dict = {
                    'username': username,
                    'mobile': mobile,
                    'level': 'VIP',
                    'eth': eth,
                }
                data = {"code": 0, "msg": "", "count": 1, "data": [user_dict]}
                return Response(data)
            elif str_type == 'level':
                if search == '粉丝':
                    try:
                        user_list = User.objects.filter(invite_num_son=invite_num, eth__lt=5)[(page - 1) * 10:page * limit]
                        count = User.objects.filter(invite_num_son=invite_num, eth__lt=5).count()
                    except:
                        return Response({"code": 0, "msg": "", "count": 0, "data": []})
                else:
                    return Response({"code": 0, "msg": "", "count": 0, "data": []})
                information = []
                for un in user_list:
                    username = un.username
                    mobile = un.mobile
                    eth = un.eth
                    user_dict = {
                        'username': username,
                        'mobile': mobile,
                        'level': '粉丝',
                        'eth': eth
                    }
                    information.append(user_dict)
                # information = information[(page - 1) * 10:page * limit]
                data = {"code": 0, "msg": "", "count": count, "data": information}
                return Response(data)
            else:
                return Response({"code": 0, "msg": "", "count": 0, "data": []})
        else:
            return Response({"code": 0, "msg": "", "count": 0, "data": []})


class ModifyView(APIView):
    def post(self, request):
        day_time = request.data.get('day_time')
        value = request.data.get('value')
        username = request.data.get('username')
        bonus = request.data.get('bonus')
        try:
            bonus_user = Bonus.objects.get(username=username, release_time=day_time)
            user = User.objects.get(username=username)
        except:
            return Response({'message': '输入错误'})
        if bonus_user.is_active == 0:
            if value == '已发放':
                bonus_user.is_active = 1
                user.eth += float(bonus)
            elif value == '未发放':
                bonus_user.is_active = 0
        else:
            return Response({'message': '输入错误'})
        user.save()
        bonus_user.save()
        return Response({'message': 'ok'})




