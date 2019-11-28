// pages/comment/comment.js
Page({

    /**
     * 页面的初始数据
     */
    data: {
        id: '',
        openID: '',
        item: {},
        comments: [],
        content:''
    },

    input:function(e){
        this.setData({
            content: e.detail.value
        })
    },

    bindFormSubmit: function (e) {
        console.log(e.detail.value)
        wx.request({
            url: 'https://www.hifn123p.cn/API/comment',
            header: {
                //请求头和ajax写法一样
                "Content-Type": "application/x-www-form-urlencoded"
            },
            method: "POST",
            data: {
                openID: this.data.openID,
                id: this.data.id,
                content: this.data.content
            },
            success: function (res) {
                console.log(res.data)
                wx.showToast({
                    title: '评论成功',
                    icon: 'none',
                    duration: 2000
                })
                this.setData({
                    content: ''
                })
            }
        })

    },

    aclickDelete: function () {
        var id = this.data.id
        console.log(id)
        var openID = this.data.openID

        wx.showModal({
            title: '确认删除？',
            content: '确认删除此条动态',
            success: function (res) {
                if (res.confirm) {
                    console.log('用户点击确定')
                    try {
                        wx.request({
                            url: 'https://www.hifn123p.cn/API/delete',
                            header: {
                                //请求头和ajax写法一样
                                "Content-Type": "application/x-www-form-urlencoded"
                            },
                            method: "POST",
                            data: {
                                openID: openID,
                                id: id,
                                type: 'a'
                            },
                            success: function (res) {
                                console.log(res.data)
                                wx.switchTab({
                                    url: '/pages/index/index'
                                })
                            }
                        })
                    } catch (e) {
                        // Do something when catch error
                    }

                } else if (res.cancel) {
                    console.log('用户点击取消')
                }
            }
        })
    },

    cclickDelete: function (e) {
        var id = e.target.id
        console.log(id)
        var openID = this.data.openID

        wx.showModal({
            title: '确认删除？',
            content: '确认删除此条评论',
            success: function (res) {
                if (res.confirm) {
                    console.log('用户点击确定')
                    try {
                        wx.request({
                            url: 'https://www.hifn123p.cn/API/delete',
                            header: {
                                //请求头和ajax写法一样
                                "Content-Type": "application/x-www-form-urlencoded"
                            },
                            method: "POST",
                            data: {
                                openID: openID,
                                id: id,
                                type: 'c'
                            },
                            success: function (res) {
                                console.log(res.data)
                                wx.switchTab({
                                    url: '/pages/index/index'
                                })
                            }
                        })
                    } catch (e) {
                        // Do something when catch error
                    }
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
        var that = this
        console.log(options)
        var id = options.r_id
        var art = {
            id: id,
            avatarUrl: options.avatarUrl,
            nickName: options.nickname,
            date: options.date,
            content: options.content,
            type: options.type,
            comments: options.comments
        }
        that.setData({
            item: art
        })
        
        get_comments(that,id)
        
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

var get_comments=function(that,id){
    var openID = wx.getStorageSync('openid')
    that.setData({ id: id, openID: openID })
    wx.request({
        url: 'https://www.hifn123p.cn/API/comments',
        header: {
            //请求头和ajax写法一样
            "Content-Type": "application/x-www-form-urlencoded"
        },
        method: "GET",
        data: {
            openID: openID,
            id: id,

        },
        success: function (res) {
            console.log(res.data)
            that.setData({ comments: res.data.comments })
        }
    })
}