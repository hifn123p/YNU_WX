from django.db import models


# Create your models here.

# 用户
class User(models.Model):
    openID = models.CharField(max_length=100, primary_key=True)  # 用户唯一id
    nickname = models.CharField(max_length=50)  # 用户名字
    avatarUrl = models.CharField(max_length=200)  # 用户头像

# dongtai
class Article(models.Model):
    openID = models.CharField(max_length=100)  # 用户唯一id
    date = models.DateTimeField(auto_now_add=True)  # 文章的发布时间
    content = models.CharField(max_length=300)  # 文章内容


class Comment(models.Model):
    r_id = models.IntegerField(default=0)  # 文章id
    openID = models.CharField(max_length=100)  # 用户唯一id
    date = models.DateTimeField(auto_now_add=True)  # 评论的发布时间
    comment = models.CharField(max_length=300)  # 评论内容
