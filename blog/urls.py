from django.urls import path
from blog import views
app_name = 'blog'
urlpatterns = [
    path('',views.home,name='home'),
    path('blog/<int:pk>',views.blog_detail,name='blog_detail'),
    path('blog_type/<int:pk>',views.blog_type,name='blog_type'),
    path('login',views.login,name='login'),
    path('userspace/<int:pk>',views.userspace,name='userspace'),
    path('write',views.write,name='write'),
    path('subcomment/<int:pk>',views.sub_comment,name='subcomment'),
    path('reply',views.reply,name='reply'),
]