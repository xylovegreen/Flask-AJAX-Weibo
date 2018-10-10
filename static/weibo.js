// Weibo API
// 获取所有微博
var apiWeiboAll = function(callback) {
    var path = '/api/weibo/all'
    ajax('GET', path, '', callback)
}

var apiWeiboAdd = function(form, callback) {
    var path = '/api/weibo/add'
    ajax('POST', path, form, callback)
}

var apiWeiboDelete = function(weibo_id, callback) {
    var path = `/api/weibo/delete?id=${weibo_id}`
    ajax('GET', path, '', callback)
}

var apiWeiboUpdate = function(form, callback) {
    var path = '/api/weibo/update'
    ajax('POST', path, form, callback)
}

var apiCommentAdd = function(form, callback) {
    var path = '/api/comment/add'
    ajax('POST', path, form, callback)
}

var apiCommentDelete = function(comment_id, callback) {
    var path = `/api/comment/delete?id=${comment_id}`
    ajax('GET', path, '', callback)
}

var apiCommentUpdate = function(form, callback) {
    var path = '/api/comment/update'
    ajax('POST', path, form, callback)
}

var commentTemplate = function(comment) {
// weibo DOM
    var c = `
        <div class="comment-cell" data-id="${comment.id}">
            <span class="comment-content">${comment.content}</span>
            <button class="comment-delete">删除</button>
            <button class="comment-edit">编辑</button>
        </div>
    `
    return c
}

var weiboTemplate = function(weibo, commentsSpan) {
// weibo DOM
    var w = `
        <div id="weibo${weibo.id}"class="weibo-cell" data-id="${weibo.id}">
            <span class="weibo-content">${weibo.content}</span>
            <button class="weibo-delete">删除</button>
            <button class="weibo-edit">编辑</button>
            <div class="weibo-comments">
            ${commentsSpan}
            </div>
            <input class="input-comment">
            <button class="button-add-comment">添加评论</button>
        </div>
    `
    return w
}

var weiboUpdateTemplate = function(content) {
// Weibo DOM
    var w = `
        <div class="weibo-update-form">
            <input class="weibo-update-input" value="${content}">
            <button class="weibo-update">更新</button>
        </div>
    `
    return w
}

var commentUpdateTemplate = function(commentContent) {
    var c = `
        <div class="comment-update-form">
            <input class="input-comment-update" value="${content}">
            <button class="button-comment-update">更新评论</button>
        </div>
    `
    return c
}

var insertWeibo = function(weibo) {
    log('weibo in insertWeibo', weibo)
    var commentsSpan = '';
    if('comments' in weibo) {
            for(var i = 0; i < weibo.comments.length; i++) {
            var comment = weibo.comments[i]
            commentsSpan += commentTemplate(comment)
        }
    }
    var weiboCell = weiboTemplate(weibo, commentsSpan)
    // 拿到所有的 comment 然后循环，把每个 comment 的 html 拼接起来
    // 插入到 weibo template 里面
    // 插入 todo-list
    var weiboList = e('#id-weibo-list')
    weiboList.insertAdjacentHTML('beforeend', weiboCell)
}

//issue: 找到 位置 插进去
var insertComment = function(comment) {
    var commentCell = commentTemplate(comment)
    weiboCell = e(`#weibo${comment.weibo_id}`)
    weiboComments = weiboCell.querySelector('.weibo-comments')
    weiboComments.insertAdjacentHTML('beforeend', commentCell)
}

var insertUpdateForm = function(content, weiboCell) {
    var updateForm = weiboUpdateTemplate(content)
    weiboCell.insertAdjacentHTML('beforeend', updateForm)
}

var loadWeibos = function() {
    apiWeiboAll(function(r) {
        console.log('load all', r)
        // 解析为 数组
        var weibos = JSON.parse(r)
        log('weibo data from ajax response', weibos)
        // 循环添加到页面中
        for(var i = 0; i < weibos.length; i++) {
            var weibo = weibos[i]
            insertWeibo(weibo)
        }
    })
}

var bindEventWeiboAdd = function() {
    var b = e('#id-button-add')
    b.addEventListener('click', function() {
        var input = e('#id-input-weibo')
        var content = input.value
        log('click add', content)
        var form = {
            content: content,
        }
        apiWeiboAdd(form, function(r){
            //将 w 显示在页面上
            var weibo = JSON.parse(r)
            //找到weibo list，插在最后
            insertWeibo(weibo)
            input.value = ''
        })
    })
}

var bindEventCommentAdd = function() {
    var weiboList = e('#id-weibo-list')
    weiboList.addEventListener('click', function(event) {
        var self = event.target
        if(self.classList.contains('button-add-comment')) {
            log('enter add comment event', self)
            weiboCell = self.closest(".weibo-cell")
            weiboId = weiboCell.dataset['id']
            input = weiboCell.querySelector('.input-comment')
            content = input.value
            log('click add', content)
            var form = {
                content: content,
                weibo_id: weiboId
            }
            apiCommentAdd(form, function(r){
                //将 w 显示在页面上
                var comment = JSON.parse(r)
                log('self in cb function in commenadd', self)
                log('weiboCell in cb function in commenadd', weiboCell)
                //找到weibo list，插在最后
                insertComment(comment)
                weiboCell = e(`#weibo${comment.weibo_id}`)
                inputSpan = weiboCell.querySelector('.input-comment')
                inputSpan.value = ''
            })
        }

    })
}

var bindEventCommentDelete = function() {
    var weiboList = e('#id-weibo-list')

    weiboList.addEventListener('click', function(event) {
      log(event)
        var self = event.target
        log('被点击的元素', self)
        if (self.classList.contains('comment-delete')) {
            log('点到了删除按钮')
            commentId = self.parentElement.dataset['id']
            apiCommentDelete(commentId, function(r){
                var r = JSON.parse(r)
                log('apiCommentDelete', r.message)
                log('self in callback function in commentdelete', self)
                self.parentElement.remove()
            })
        } else {
            log('点到了 weibo list')
        }
    })
}


var bindEventCommentEdit = function() {
    var b = e('#id-weibo-list')
    b.addEventListener('click', function(event) {
        var self = event.target
        if (self.classList.contains('comment-edit')) {
            commentCell = self.parentElement
            content = commentCell.querySelector('.comment-content').innerText
            updateForm = commentUpdateTemplate(content)
            commentCell.insertAdjacentHTML('beforeend', updateForm)
        }
        })
}

var bindEventCommentUpdate = function() {
    var weiboList = e('#id-weibo-list')
    weiboList.addEventListener('click', function(event) {
    log(event)
    var self = event.target
    log('被点击的元素', self)
    log(self.classList)
    if (self.classList.contains('button-comment-update')) {
        log('点到了更新按钮')
        commentCell = self.closest('.comment-cell')
        commentId = commentCell.dataset['id']
        log('update comment id', commentId)
        input = commentCell.querySelector('.input-comment-update')
        content = input.value
        var form = {
            id: commentId,
            content: content,
        }

        apiCommentUpdate(form, function(r) {
            // 收到返回的数据, 插入到页面中
            var comment = JSON.parse(r)
            log('apiCommentUpdate', comment)

            var commentSpan = commentCell.querySelector('.comment-content')
            commentSpan.innerText = comment.content

            var updateForm = commentCell.querySelector('.comment-update-form')
            updateForm.remove()
        })
    } else {
        log('点到了 todo cell')
    }
})}

var bindEventWeiboDelete = function() {
    var weiboList = e('#id-weibo-list')

    weiboList.addEventListener('click', function(event) {
      log(event)
        var self = event.target
        log('被点击的元素', self)
        if (self.classList.contains('weibo-delete')) {
            log('点到了删除按钮')
            weiboId = self.parentElement.dataset['id']
            apiWeiboDelete(weiboId, function(r){
                var r = JSON.parse(r)
                log('apiWeiboDelete', r.message)
                log('self in callback function in weibodelete', self)
                self.parentElement.remove()
            })
        } else {
            log('点到了 weibo list')
        }
    })
}

var bindEventWeiboEdit = function() {
    var weiboList = e('#id-weibo-list')
    weiboList.addEventListener('click', function(event) {
    log(event)
    var self = event.target
    log('被点击的元素', self)
    log(self.classList)
    if (self.classList.contains('weibo-edit')) {
        log('点到了编辑按钮')
        weiboCell = self.closest('.weibo-cell')
        weiboId = weiboCell.dataset['id']
        var weiboSpan = weiboCell.querySelector('.weibo-content')
        var content = weiboSpan.innerText
        // 插入编辑输入框
        insertUpdateForm(content, weiboCell)
    } else {
        log('点到了 weibo cell')
    }
})}

var bindEventWeiboUpdate = function() {
    var weiboList = e('#id-weibo-list')
    weiboList.addEventListener('click', function(event) {
    log(event)
    var self = event.target
    log('被点击的元素', self)
    // 通过比较被点击元素的 class
    // 来判断元素是否是我们想要的
    // classList 属性保存了元素所有的 class
    log(self.classList)
    if (self.classList.contains('weibo-update')) {
        log('点到了更新按钮')
        weiboCell = self.closest('.weibo-cell')
        weiboId = weiboCell.dataset['id']
        log('update weibo id', weiboId)
        input = weiboCell.querySelector('.weibo-update-input')
        content = input.value
        var form = {
            id: weiboId,
            content: content,
        }

        apiWeiboUpdate(form, function(r) {
            // 收到返回的数据, 插入到页面中
            var weibo = JSON.parse(r)
            log('apiWeiboUpdate', weibo)

            var weiboSpan = weiboCell.querySelector('.weibo-content')
            weiboSpan.innerText = weibo.content

            var updateForm = weiboCell.querySelector('.weibo-update-form')
            updateForm.remove()
        })
    } else {
        log('点到了 todo cell')
    }
})}

var bindEvents = function() {
    bindEventWeiboAdd()
    bindEventWeiboEdit()
    bindEventWeiboUpdate()
    bindEventWeiboDelete()
    bindEventCommentAdd()
    bindEventCommentDelete()
    bindEventCommentEdit()
    bindEventCommentUpdate()
}

var __main = function() {
    bindEvents()
    loadWeibos()
}

__main()
