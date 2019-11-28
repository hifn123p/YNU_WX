// pages/user_bind/user_bind.js
var util = require('/../../utils/util.js');
Page({

    /**
     * 页面的初始数据
     */
    data: {
        user: "",
        password: "",
        stu_name: '',
        isbind: false,
        loading1: false,
        loading2: false,
    },

    /**
     *  获取输入框的学号，密码
     */
    user: function (event) {
        this.setData({ user: event.detail.value })
        try {
            wx.setStorageSync('username', this.data.user)
        } catch (e) {
        }
    },
    password: function (event) {
        this.setData({ password: event.detail.value })
    },


    /**
     * 绑定教务系统
     * 提交学号，密码，成功，设置缓存
     * 进入绑定信息页
     */
    login: function () {
        var that = this
        if (that.data.user == '' || that.data.password == '') {
            wx.showToast({
                title: '学号密码不能为空',
                icon: 'none',
                duration: 2000
            })
        } else {
            that.setData({ loading1: true })
            try {
                wx.request({
                    url: 'https://www.hifn123p.cn/API/bind',
                    header: {
                        //请求头和ajax写法一样
                        "Content-Type": "application/x-www-form-urlencoded"
                    },
                    method: "POST",
                    data: { username: that.data.user, password: that.data.password },
                    success: function (res) {
                        if (res.data.msg == '0') {
                            wx.showToast({
                                title: '绑定失败',
                                icon: 'none',
                                duration: 2000
                            })
                            that.setData({ loading1: false })
                        } else {
                            wx.showToast({
                                title: '成功',
                                icon: 'success',
                                duration: 2000
                            })
                            console.log(res)
                            that.setData({ isbind: true })
                            wx.setStorageSync('isbind', true)
                            wx.setStorageSync('mydata', res.data)

                            bindsucce(that)
                            
                        }
                    }
                })
            } catch (e) {
            }
        }
    },


    /**
     * 解绑定教务系统，成功，修改缓存,删除学号
     * 进入user页
     */
    loginout: function () {
        this.setData({ loading2: true })
        try {
            wx.setStorageSync('isbind', false)
            wx.removeStorageSync('username')
            wx.removeStorageSync("mydata")
        } catch (e) {
        }
        wx.switchTab({
            url: '/pages/user/user'
        })
    },


    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function (options) {
        console.log("onload user_bind" + this.data.isbind)

    },

    /**
     * 生命周期函数--监听页面初次渲染完成
     */
    onReady: function () {

    },

    /**
     * 生命周期函数--监听页面显示
     */
    onShow: function () {
        // 获取本地缓存数据
        var that = this
        bindsucce(that)
    },

    /**
     * 生命周期函数--监听页面隐藏
     */
    onHide: function () {
        console.log("app onhide")
    },

    /**
     * 生命周期函数--监听页面卸载
     */
    onUnload: function () {
        console.log("app onunload")
    },

    /**
     * 页面相关事件处理函数--监听用户下拉动作
     */
    onPullDownRefresh: function () {

    },

    /**
     * 页面上拉触底事件的处理函数
     */
    onReachBottom: function () {

    },

    /**
     * 用户点击右上角分享
     */
    onShareAppMessage: function () {

    }
})

var bindsucce = function (that) {
    try {
        var isbind = wx.getStorageSync('isbind')
        //绑定之后
        if (isbind) {
            var username = wx.getStorageSync('username')
            var stu_name = wx.getStorageSync('mydata').stu_name
            var mydata = wx.getStorageSync('mydata')
            var name = wx
            that.setData({ isbind: isbind, user: username, stu_name: stu_name, mydata: mydata })
        }
    } catch (e) {

    }
    console.log(that.data.isbind + "  user_bind onshow isbind")
}