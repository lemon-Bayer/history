var vm = new Vue({
	el: '#app',
	data: {
		host : host,
		error_phone: false,
		error_sms_code: false,
        sending_flag: false,
		error_sms_code_message: '',
		error_phone_message: '',

		sms_code_tip: '获取短信验证码',
		mobile: '',
		sms_code: ''
	},

	methods: {
        // 获取url路径参数
        get_query_string: function(name){
            var reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)', 'i');
            var r = window.location.search.substr(1).match(reg);
            if (r != null) {
                return decodeURI(r[2]);
            }
            return null;
        },
		// 检查手机号
        check_phone: function () {
            var re = /^1[3456789]\d{9}$/;
            if (re.test(this.mobile)) {
                axios.get(this.host + '/mobiles/' + this.mobile + '/count/', {
                    responseType: 'json'
                })
                    .then(response => {
                        if (response.data.count == 0) {
                            this.error_phone_message = '账号不存在';
                            this.error_phone = true;
                        } else {
                            this.error_phone = false;
                        }
                    })
                    .catch(error => {
                        console.log(error.response.data);
                    })
            } else {
                this.error_phone_message = '您输入的手机号格式不正确';
                this.error_phone = true;
            }
        },
        check_sms_code: function () {
            if (!this.sms_code) {
                this.error_sms_code_message = '请填写短信验证码';
                this.error_sms_code = true;
            } else {
                this.error_sms_code = false;
            }
        },
		// 发送手机短信验证码
        send_sms_code: function(){
            this.check_phone();
            if (this.error_phone == false && this.sending_flag == false) {
                this.sending_flag = true;
                axios.get(this.host + '/sms_codes/' + this.mobile, {
                    responseType: 'json'
                })
                    .then(response => {
                        if (response.data.message == 'ok') {
                            // 表示后端发送短信成功
                            // 倒计时60秒，60秒后允许用户再次点击发送短信验证码的按钮
                            var num = 60;
                            // 设置一个计时器
                            var t = setInterval(() => {
                                if (num == 1) {
                                    // 如果计时器到最后, 清除计时器对象
                                    clearInterval(t);
                                    // 将点击获取验证码的按钮展示的文本回复成原始文本
                                    this.sms_code_tip = '获取短信验证码';
                                    // 将点击按钮的onclick事件函数恢复回去
                                    this.sending_flag = false;
                                } else {
                                    num -= 1;
                                    // 展示倒计时信息
                                    this.sms_code_tip = num + '秒';
                                    this.sending_flag = true
                                }
                            }, 1000, 60)
                        } else {
                            var num = 10;
                            // 设置一个计时器
                            var t = setInterval(() => {
                                if (num == 1) {
                                    // 如果计时器到最后, 清除计时器对象
                                    clearInterval(t);
                                    // 将点击获取验证码的按钮展示的文本回复成原始文本
                                    this.sms_code_tip = '获取短信验证码';
                                    // 将点击按钮的onclick事件函数恢复回去
                                    this.sending_flag = false;
                                } else {
                                    num -= 1;
                                    // 展示倒计时信息
                                    this.sms_code_tip = '发送失败' + num + '秒';
                                }
                            }, 1000, 10)
                        }
                    })

            }
        },
		// 登录
		on_submit: function(){
			this.check_phone();
			this.check_sms_code();

            if (this.error_phone == false && this.error_sms_code == false) {
                axios.post(this.host + '/authorizations/', {
                    mobile: this.mobile,
                    sms_code: this.sms_code
                }, {
                    responseType: 'json',
                    withCredentials: true
                })
                    .then(response => {
                    // 记录用户的登录状态
                    sessionStorage.clear();
                    localStorage.clear();
                    localStorage.token = response.data.token;
                    localStorage.cliname = response.data.username;
                    localStorage.is_staff = response.data.is_staff;
                    localStorage.level = response.data.level;
                    if(response.data.is_staff){
                        layer.msg('登录成功');
                       	setTimeout(function(){
			              location.href = 'admin1.html';
			            },2000);

                    } else{
                        layer.msg('登录成功');
                        setTimeout(function(){
                          location.href = 'member.html';
			            },2000);
                    }
                    })
                    .catch(error => {
                        if (error.response.status == 400) {
                            if ('non_field_errors' in error.response.data) {
                                this.error_sms_code_message = error.response.data.non_field_errors[0];
                            } else {
                                this.error_sms_code_message = '数据有误';
                            }
                            this.error_sms_code = true;
                        } else {
                            console.log(error.response.data);
                        }
                    })
            }
        }
    }
});
