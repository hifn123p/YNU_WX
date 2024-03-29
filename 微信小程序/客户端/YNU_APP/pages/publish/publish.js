// pages/publish/publish.js
Page({

    /**
     * 页面的初始数据
     */
    data: {
    },
    
    bindFormSubmit: function (e) {
        console.log(e.detail.value.textarea)
        var openID = wx.getStorageSync('openid')
        wx.request({
            url: 'https://www.hifn123p.cn/API/publish',
            header: {
                //请求头和ajax写法一样
                "Content-Type": "application/x-www-form-urlencoded"
            },
            method: "POST",
            data: {
                openID: openID,
                content: e.detail.value.textarea
            },
            success: function (res) {
                console.log(res.data)
                wx.showToast({
                    title: '发表成功',
                    icon: 'none',
                    duration: 2000
                })
                wx.switchTab({
                    url: '/pages/index/index'
                })

            }
        })
    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function (options) {

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