from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey,GenericRelation
from django.shortcuts import reverse
import os
# Create your models here.

class ArticleType(models.Model):
    article_type = models.CharField('文章类型',max_length=20)
    class Meta:
        verbose_name = '文章类型'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.article_type


class Article(models.Model):
    title = models.CharField('标题',max_length = 50)
    article_type = models.ForeignKey(ArticleType,on_delete=models.CASCADE,verbose_name='文章类型')
    author = models.ForeignKey(User,on_delete = models.CASCADE,verbose_name = '作者')  
    created_date = models.DateTimeField('创建时间',auto_now_add = True)
    last_revise = models.DateTimeField('上次修改时间',auto_now = True)
    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-created_date']
    
    def get_face_img(self):
        if not hasattr(self,'faceimg'):
            return 'faceimg.jpg'
        else:
            return self.faceimg

    def __str__(self):
        return self.title


class Content(models.Model):
    content = models.TextField('文章内容')
    article = models.OneToOneField(Article,on_delete=models.CASCADE,verbose_name = '文章')
    class Meta:
        verbose_name = '文章内容'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.content


class Comment(models.Model):
    parent = models.ForeignKey('self',null=True,blank=True,on_delete=models.CASCADE)
    article = models.ForeignKey(Article,on_delete=models.CASCADE,null=True,blank=True)
    created_time = models.DateTimeField('评论时间',auto_now_add=True)
    rid = models.ForeignKey(User,on_delete=True,verbose_name='回复人',related_name='mycomments')
    pid = models.ForeignKey(User,on_delete=True,null=True,blank=True,verbose_name='被回复人')
    content = models.TextField('评论内容')

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.content


class FaceImg(models.Model):
    article = models.OneToOneField(Article,on_delete=models.CASCADE)
    path = models.CharField('路径',max_length=30)

    class Meta:
        verbose_name = '封面'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.path


class Avatar(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    path = models.CharField('路径',max_length=30)

    class Meta:
        verbose_name = '头像'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.path