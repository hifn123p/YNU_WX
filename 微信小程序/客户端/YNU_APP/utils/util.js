const formatTime = date => {
  const year = date.getFullYear()
  const month = date.getMonth() + 1
  const day = date.getDate()
  const hour = date.getHours()
  const minute = date.getMinutes()
  const second = date.getSeconds()

  return [year, month, day].map(formatNumber).join('-') + ' ' + [hour, minute, second].map(formatNumber).join(':')
}

const formatNumber = n => {
  n = n.toString()
  return n[1] ? n : '0' + n
}

// 获取本地缓存大小
function getstoragesize(that){
    wx.getStorageInfo({
        success: function (res) {
            var size = res.currentSize
            that.setData({ storagesize: size })
        },
    })
}


module.exports = {
  formatTime: formatTime,
  getstoragesize: getstoragesize,
}
