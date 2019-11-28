from django.shortcuts import render
from django.http.response import HttpResponse
from API import data, wx, utils
from django.views.decorators.csrf import csrf_exempt
"""
请求模块
"""


# wx openID
def openid(request):
    if request.method == 'GET':
        code = request.GET.get('code', '')
        openid = wx.open_id(code)

        return HttpResponse(openid)

@csrf_exempt
def save(request):
    if request.method == 'GET':
        openid = request.GET.get('openID')
        nickname = request.GET.get('nickname')
        avatarUrl = request.GET.get('avatarUrl')

        utils.user_save(openid, nickname, avatarUrl)
        return HttpResponse('ok')
    if request.method == 'POST':
        openid = request.POST.get('openID')
        nickname = request.POST.get('nickname')
        avatarUrl = request.POST.get('avatarUrl')

        utils.user_save(openid, nickname, avatarUrl)
        return HttpResponse('ok')


# 获取主页动态
def index(request):
    if request.method == 'GET':
        openid = request.GET.get('openID')

        article_json = utils.parse_article(openid)

        return HttpResponse(article_json)


# 获取评论 需要文章id
def get_comments(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        openid = request.GET.get('openID')
        comments_json = utils.parse_comments(id, openid)

        return HttpResponse(comments_json)


# 发表模块  需要openid  文章内容content
@csrf_exempt
def publish(request):
    if request.method == 'GET':
        openid = request.GET.get('openID')
        content = request.GET.get('content')
        utils.content_save(openid, content)

        return HttpResponse('ok')
    if request.method == 'POST':
        openid = request.POST.get('openID')
        content = request.POST.get('content')

        utils.content_save(openid, content)

        return HttpResponse('ok')


# 评论模块  需要openid 文章id 评论内容content
@csrf_exempt
def comment(request):
    if request.method == 'GET':
        openid = request.GET.get('openID')
        id = request.GET.get('id')
        content = request.GET.get('content')

        utils.comment_save(openid, id, content)

        return HttpResponse('ok')
    if request.method == 'POST':
        openid = request.POST.get('openID', '')
        id = request.POST.get('id', '')
        content = request.POST.get('content', '')

        utils.comment_save(openid, id, content)

        return HttpResponse('ok')


# 删除模块  需要openid  文章id
@csrf_exempt
def delete(request):
    if request.method == 'GET':
        openid = request.GET.get('openID')
        id = request.GET.get('id')
        type = request.GET.get('type')
        id=int(id)
        
        if type == 'a':
            utils.article_delete(openid, id)
        if type == 'c':
            utils.comment_delete(openid, id)

        return HttpResponse('ok')
    if request.method == 'POST':
        openid = request.POST.get('openID')
        id = request.POST.get('id')
        type = request.POST.get('type')

        if type == 'a':
            utils.article_delete(openid, id)
        if type == 'c':
            utils.comment_delete(openid, id)

        return HttpResponse(openid+'+'+id+type)


# 绑定模块
@csrf_exempt
def bind(request):
    if request.method == 'GET':
        username = request.GET.get('username', '')
        password = request.GET.get('password', '')
        ynu_json = data.main(username, password)
        return HttpResponse(ynu_json)
    else:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        ynu_json = data.main(username, password)
        return HttpResponse(ynu_json)
