var vm = new Vue({
	el: '#app',
	data: {
	    host: host,
        error_name: false,
		error_invite_num: false,
		error_purse_addr: false,
		error_phone: false,
		error_sms_code: false,
        error_name_message: '',
		error_sms_code_message: '',
		error_phone_message: '',
		error_invite_num_message: '',
		error_purse_addr_message: '',
        send_flag: false,
		sms_code_tip: '获取短信验证码',
		sending_flag: false,
        username: '',
		invite_num_son: '',
		purse_addr: '',
		mobile: '',
		sms_code: ''
	},

	methods: {
		check_invite_num: function (){
			var len = this.invite_num_son.length;
			if(len<4||len>6) {
				this.error_invite_num_message = '请输入正确邀请码';
				this.error_invite_num = true;
			} else {
				axios.get(this.host + '/invite/num/' + this.invite_num_son + '/count/', {
					responseType: 'json'
				})
					.then(response => {
						if(response.data.count == 0){
							this.error_invite_num_message = '邀请码不存在';
							this.error_invite_num = true;
						}else{
							this.error_invite_num = false;
						}
					})
					.catch(error => {
						console.log(error.response.data);
					})
			}
		},
        // 检查用户名
        check_username: function () {
            var len = this.username.length;
            if (len < 5 || len > 20) {
                this.error_name_message = '请输入5-20个字符的用户名';
                this.error_name = true;
            } else {
                axios.get(this.host + '/usernames/' + this.username + '/count/', {
                    responseType: 'json'
                })
                    .then(response => {
                        if (response.data.count > 0) {
                            this.error_name_message = '用户名已存在';
                            this.error_name = true;
                        } else {
                            this.error_name = false;
                        }
                    })
                    .catch(error => {
                        console.log(error.response.data);
                    })
            }
        },
		check_purse_addr: function (){
			var re = /^0x[a-zA-Z0-9]{40}$/;
			if(re.test(this.purse_addr)){
				axios.get(this.host + '/purse/addr/' + this.purse_addr + '/count/', {
					responseType: 'json'
				})
					.then(response => {
						if(response.data.count > 0){
							this.error_purse_addr_message = '钱包地址已存在';
							this.error_purse_addr = true;
						}else{
							this.error_purse_addr = false;
						}
					})
					.catch(error => {
						console.log(error.response.data);
					})
			} else {
				this.error_purse_addr_message = '输入的钱包地址格式不对';
				this.error_purse_addr = true;
			}
		},
		// 检查手机号
        check_phone: function () {
            var re = /^1[3456789]\d{9}$/;
            if (re.test(this.mobile)) {
                axios.get(this.host + '/mobiles/' + this.mobile + '/count/', {
                    responseType: 'json'
                })
                    .then(response => {
                        if (response.data.count > 0) {
                            this.error_phone_message = '手机号已存在';
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
        send_sms_code: function () {
            // 校验参数，保证输入框有数据填写
            this.check_phone();
            // 向后端接口发送请求，让后端发送短信验证码
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

		// 注册
		on_submit: function(){
			this.check_invite_num();
            this.check_username();
			this.check_purse_addr();
			this.check_phone();
			this.check_sms_code();

            if (this.error_name == false && this.error_invite_num == false && this.error_purse_addr == false && this.error_phone == false && this.error_sms_code == false) {
                axios.post(this.host + '/users/', {
                    username: this.username,
                    purse_addr: this.purse_addr,
                    invite_num_son: this.invite_num_son,
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
                        layer.msg('注册成功');
                       	setTimeout(function(){
			              location.href = 'admin1.html';
			            },1000);

                    } else{
                        layer.msg('注册成功');
                        setTimeout(function(){
                          location.href = 'member.html';
			            },1000);
                    }
                    })
                    .catch(error => {
                        if (error.response.status == 400) {
                            if ('non_field_errors' in error.response.data) {
                                this.error_sms_code_message = error.response.data.non_field_errors[0];
                            } else {
                                this.error_sms_code_message = '数据有误';
                                this.error_invite_num_message = '数据有误';
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
