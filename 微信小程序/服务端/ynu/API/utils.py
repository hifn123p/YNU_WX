import json
from datetime import date
from datetime import datetime
from django.core import serializers
from wx_api.models import Article, User, Comment
from django.core.serializers.json import DjangoJSONEncoder


def parse_article(openID):
    data = {'msg': '', 'article': []}

    all_article = Article.objects.values()
    for i in range(len(all_article)):
        openid = all_article[i].get('openID')
        type = 0

        if openid == openID:
            type = 1

        user = User.objects.filter(openID=openid).values()[0]
        nickname = user.get('nickname')
        avatarUrl = user.get('avatarUrl')

        id = all_article[i].get('id')
        date = all_article[i].get('date')
        content = all_article[i].get('content')

        comments = Comment.objects.filter(r_id=id).count()

        article = {'id': id,
                   'nickname': nickname,
                   'avatarUrl': avatarUrl,
                   'date': date,
                   'content': content,
                   'comments': comments,
                   'type': type
                   }

        data['article'].append(article)

    article_json = json.dumps(data, ensure_ascii=False, cls=JsonCustomEncoder)
    return article_json


def parse_comments(r_id, openID):
    data = {'msg': '', 'comments': []}

    all_comment = Comment.objects.filter(r_id=r_id).values()
    for i in range(len(all_comment)):
        openid = all_comment[i].get('openID')
        print(openid)
        type = 0

        if openid == openID:
            type = 1

        id = all_comment[i].get('id')

        user = User.objects.filter(openID=openid).values()[0]
        nickname = user.get('nickname')
        avatarUrl = user.get('avatarUrl')
        date = all_comment[i].get('date')
        comment = all_comment[i].get('comment')

        comments = {'id': id,
                    'nickname': nickname,
                    'avatarUrl': avatarUrl,
                    'date': date,
                    'content': comment,
                    'type': type
                    }

        data['comments'].append(comments)

    comments_json = json.dumps(data, ensure_ascii=False, cls=JsonCustomEncoder)
    return comments_json


def content_save(openID, content):
    art = Article(openID=openID, content=content)
    art.save()


def comment_save(openID, r_id, comment):
    com = Comment(openID=openID, r_id=r_id, comment=comment)
    com.save()


def article_delete(openID, id):
    Article.objects.filter(id=id, openID=openID).delete()
    Comment.objects.filter(r_id=id).delete()


def comment_delete(openID, id):
    Comment.objects.filter(id=id, openID=openID).delete()


def user_save(openID, nickname, avatarUrl):
    user = User(openID=openID, nickname=nickname, avatarUrl=avatarUrl)
    user.save()


class JsonCustomEncoder(json.JSONEncoder):

    def default(self, field):

        if isinstance(field, datetime):
            return field.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(field, date):
            return field.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, field)
