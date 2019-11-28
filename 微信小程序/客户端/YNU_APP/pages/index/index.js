const app = getApp()
Page({

    /**
     * 页面的初始数据
     */
    data: {
        imgUrls: [
            'http://www.news.ynu.edu.cn/__local/E/19/BC/EF71458D76AF8D555DEE75944CF_DEEABA5D_32526.jpg',
            'http://www.news.ynu.edu.cn/images/1DX22680.jpg',
            'http://www.ynu.edu.cn/0000.jpg'
        ],
        list: [],
    },
    pb: function () {
        if (app.globalData.userInfo) {
            wx.navigateTo({
                url: '/pages/publish/publish'
            })
        } else {
            wx.showToast({
                title: '请登录',
                icon: 'none',
                duration: 2000
            })
        }
    },
    
    imgOnclick: function (e) {
        var u=e.target.dataset.url
        wx.previewImage({
            urls: [u],
        })
    },

    clickDelete: function (e) {
        var id = e.target.id
        console.log(e)
        var openID = wx.getStorageSync('openid')

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


    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function (options) {

    },

    // /**
    //  * 生命周期函数--监听页面初次渲染完成
    //  */
    // onReady: function () {

    // },

    /**
     * 生命周期函数--监听页面显示
     */
    onShow: function () {
        var that = this
        get_article(that)
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

var get_article = function (that) {
    var openID = wx.getStorageSync('openid')
    wx.request({
        url: 'https://www.hifn123p.cn/API/index',
        header: {
            //请求头和ajax写法一样
            "Content-Type": "application/x-www-form-urlencoded"
        },
        method: "GET",
        data: {
            openID: openID
        },
        success: function (res) {
            console.log(res.data)
            that.setData({ list: res.data.article.reverse() })
        }
    })
}