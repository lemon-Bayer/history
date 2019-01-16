var vm = new Vue({
    el: '#app',
    data: {
        host,
        user_id: sessionStorage.user_id || localStorage.user_id,
        token: sessionStorage.token || localStorage.token,
        city_num: '',
        vip_num: '',
        member_num: '',
        fans_num: '',
    },
    mounted: function () {
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
                    this.city_num = response.data.city_num;
                    this.vip_num = response.data.vip_num;
                    this.member_num = response.data.member_num;
                    this.fans_num = response.data.fans_num;
                })
                .catch(error => {
                    if (error.response.status == 401 || error.response.status == 403) {
                        location.href = '/index.html?next=/admin1.html';
                    }
                });
        } else {
            location.href = '/index.html?next=/admin1.html';
        }
    },
    methods: {
        // 退出
        logout: function () {
            sessionStorage.clear();
            localStorage.clear();
            location.href = '/login.html';
        },
    }
});
