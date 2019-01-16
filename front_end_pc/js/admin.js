/**
 * Created by python on 18-9-27.
 */
var vm = new Vue({
    el: '#app',
    data: {
        host,
        user_id: sessionStorage.user_id || localStorage.user_id,
        token: sessionStorage.token || localStorage.token,
        username:'',
        mobile: '',
        level: '',
        invite_per_num: '',
        eth: '',
        dlb: '',
        bonus: '',
        city_num: '',
        vip_num: '',
        member_num: '',
        fans_num: '',
        yday_investment: '',
        day_investment: '',
        yday_send_bonus: '',
        day_send_bonus: '',
    },
    mounted: function(){
        // 判断用户的登录状态
        if (this.user_id && this.token) {
            axios.get(this.host + '/user/', {
                    // 向后端传递JWT token的方法
                    headers: {
                        'Authorization': 'JWT ' + this.token
                    },
                    responseType: 'json',
                })
                .then(response => {
                    // 加载用户数据
                    this.username = response.data.username;
                    this.mobile = response.data.mobile;
                    this.level = response.data.level;
                    this.invite_per_num = response.data.invite_per_num;
                    this.eth = response.data.eth;
                    this.dlb = response.data.dlb;
                    this.city_num = response.data.city_num;
                    this.vip_num = response.data.vip_num;
                    this.member_num = response.data.member_num;
                    this.fans_num = response.data.fans_num;
                    this.yday_investment = response.data.yday_investment;
                    this.day_investment = response.data.day_investment;
                    this.yday_send_bonus = response.data.yday_send_bonus;
                    this.day_send_bonus = response.data.day_send_bonus;
                })
                .catch(error => {
                    if (error.response.status==401 || error.response.status==403) {
                        location.href = '/index.html?next=/admin1.html';
                    }
                });
        } else {
            location.href = '/index.html?next=/admin1.html';
        }
    },
    methods: {
        // 退出
        logout: function(){
            sessionStorage.clear();
            localStorage.clear();
            location.href = '/login.html';
        },
        // 保存email
        save_email: function(){
            var re = /^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/;
            if(re.test(this.email)) {
                this.email_error = false;
            } else {
                this.email_error = true;
                return;
            }
            axios.put(this.host + '/emails/',
                { email: this.email },
                {
                    headers: {
                        'Authorization': 'JWT ' + this.token
                    },
                    responseType: 'json'
                })
                .then(response => {
                    this.set_email = false;
                    this.send_email_btn_disabled = true;
                    this.send_email_tip = '已发送验证邮件'
                })
                .catch(error => {
                    alert(error.data);
                });
        }
    }
});