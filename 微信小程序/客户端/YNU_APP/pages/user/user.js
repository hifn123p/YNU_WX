// pages/user/user.js
const app = getApp()
var util = require('/../../utils/util.js');

Page({

    /**
     * 页面的初始数据
     */
    data: {
        isbind: '未绑定',
        storagesize: '0',
        msg: true,
        userInfo: {},
        hasUserInfo: false,
        canIUse: wx.canIUse('button.open-type.getUserInfo'),

    },


    //事件处理函数
    bindViewTap: function () {
        wx.navigateTo({
            url: '../logs/logs'
        })
    },

    //跳转绑定页面
    btnbind: function () {
        if (this.data.userInfo.nickName) {
            wx.navigateTo({
                url: '/pages/user_bind/user_bind'
            })
        } else {
            wx.showToast({
                title: '请登录',
                icon: 'none',
                duration: 2000
            })
        }
    },

    // 清楚本地缓存
    clean: function (e) {
        var that = this
        wx.showModal({
            title: '确认清楚数据？',
            content: '将清楚所有数据包括课表成绩信息',
            success: function (res) {
                if (res.confirm) {
                    console.log('用户点击确定')
                    try {
                        wx.removeStorageSync('logs')
                        wx.removeStorageSync('mydata')
                        wx.removeStorageSync('username')
                        wx.removeStorageSync('isbind')

                    } catch (e) {
                        // Do something when catch error
                    }
                    //重新查询缓存大小
                    util.getstoragesize(that)
                } else if (res.cancel) {
                    console.log('用户点击取消')
                }
            }
        })
    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function (options) {
        if (app.globalData.userInfo) {
            this.setData({
                userInfo: app.globalData.userInfo,
                hasUserInfo: true
            })
        } else if (this.data.canIUse) {
            // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
            // 所以此处加入 callback 以防止这种情况
            app.userInfoReadyCallback = res => {
                this.setData({
                    userInfo: res.userInfo,
                    hasUserInfo: true
                })
            }
        } else {
            // 在没有 open-type=getUserInfo 版本的兼容处理
            wx.getUserInfo({
                success: res => {
                    app.globalData.userInfo = res.userInfo
                    this.setData({
                        userInfo: res.userInfo,
                        hasUserInfo: true
                    })
                }
            })
        }

    },
    getUserInfo: function (e) {
        console.log(e)
        app.globalData.userInfo = e.detail.userInfo
        if (e.detail.errMsg == "getUserInfo:fail auth deny") {
            this.setData({
                msg: false,
            })
            console.log(this.data.msg + "授权失败")
        } else {
            this.setData({
                userInfo: e.detail.userInfo,
                hasUserInfo: true,
                msg: true,
            })
            console.log(this.data.msg + "授权成功")
            var openID = wx.getStorageSync('openid')
            wx.request({
                url: 'https://www.hifn123p.cn/API/save',
                header: {
                    //请求头和ajax写法一样
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                method: "POST",
                data: {
                    openID: openID,
                    nickname: this.data.userInfo.nickName,
                    avatarUrl: this.data.userInfo.avatarUrl
                },
                success: function (res) {
                    console.log(res.data)
                }
            })
        }

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

        // 获取本地缓存大小
        util.getstoragesize(that)
        try {
            var isbind = wx.getStorageSync('isbind')
            var user = this.data.userInfo.nickName
            if (isbind == true && user) {
                that.setData({ isbind: "绑定" })
            }
            else if (isbind == false) {
                that.setData({ isbind: "未绑定" })
            }
        } catch (e) {

        }

    },

    /**
     * 生命周期函数--监听页面隐藏
     */
    onHide: function () {

    },

    /**
     * 生命周期函数--监听页面卸载
     */
    onUnload: function () {

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