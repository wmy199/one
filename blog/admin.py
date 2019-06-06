from django.contrib import admin
from blog.models import Article,ArticleType,Comment,Content,FaceImg
# Register your models here.
@admin.register(Article)
class AuticleAdmin(admin.ModelAdmin):
    list_display = ('title','article_type','author','created_date','last_revise')
    date_hierarchy = 'last_revise'

@admin.register(ArticleType)
class ArticleTypeAdmin(admin.ModelAdmin):
    list_display = ('article_type',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('parent','article','created_time','rid','pid')

@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('content','article')

@admin.register(FaceImg)
class FaceImgAdmin(admin.ModelAdmin):
    list_display = ('path','article')