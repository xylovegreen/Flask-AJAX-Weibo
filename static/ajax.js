var log = console.log.bind(console)

var e = function(sel) {
    return document.querySelector(sel)
}

/*
 ajax 函数
*/
var ajax = function(method, path, data, responseCallback) {
    var r = new XMLHttpRequest()
    // 设置请求方法和请求地址
    r.open(method, path, true)
    // 设置发送的数据的格式为 application/json
    // 这个不是必须的 因为规定了前后端都发送 json 格式的数据
    r.setRequestHeader('Content-Type', 'application/json')
    // 注册响应函数
    r.onreadystatechange = function() {
        if(r.readyState === 4) {
            // r.response 就是服务器发过来的放在 HTTP BODY 中的数据
            responseCallback(r.response)
        }
    }
    // 把数据转换为 json 格式字符串
    log('data before stringify in AJAX', data)
    data = JSON.stringify(data)
    log('AJAX send data', data)
    // 发送请求
    r.send(data)
}
