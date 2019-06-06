from django.shortcuts import render,get_object_or_404,redirect,reverse
from django.core.paginator import Paginator
from django.http import HttpResponse,JsonResponse,Http404
from django.contrib.auth import authenticate
from django.contrib.auth import login as _login
from django.contrib.auth.models import User
from mysite import settings
import json
from blog import models
import os
# Create your views here.







def home(request):
    article = models.Article.objects.all()
    paginator = Paginator(article,10)
    page = request.GET.get('page',1)
    page = paginator.get_page(page)
    page_range = range(max(page.number-2,1),min(page.number+2+1,paginator.num_pages+1))

    return render(request,'home.html',{'page':page,'page_range':page_range})
    #return HttpResponse('{"s":"s","w":5}',"application.json")

def reply(request):
    if not request.user.is_authenticated:
        return HttpResponse('IS NOT LOGIN')
    print(request.method)
    print(request.POST.get('parent'))
    if request.POST.get('article'):
        models.Comment(article=get_object_or_404(models.Article,pk=request.POST.get('article'))
                        ,rid=request.user
                        ,content=request.POST.get('content')
        ).save()
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        models.Comment(parent=get_object_or_404(models.Comment,pk=request.POST.get('parent'))
                        ,rid=request.user
                        ,pid=get_object_or_404(User,pk=request.POST.get('pid'))
                        ,content=request.POST.get('content')
        ).save()
        return redirect(request.META.get('HTTP_REFERER'))
    
def sub_comment(request,pk):
    comment = get_object_or_404(models.Comment,pk=pk)
    paginator = Paginator(comment.comment_set.all(),10)
    page = request.GET.get('page',1)
    page = paginator.get_page(page)
    page_range = range(max(page.number-2,1),min(page.number+2+1,paginator.num_pages+1))
    return render(request,'subcomment_ajax.html',{'page':page,'page_range':page_range})

def blog_detail(request,pk):
    if request.method == 'GET':
        article =  get_object_or_404(models.Article,pk=pk)
        paginator = Paginator(article.comment_set.all(),10)
        page = request.GET.get('page',1)
        page = paginator.get_page(page)
        page_range = range(max(page.number-2,1),min(page.number+2+1,paginator.num_pages+1))
        if request.is_ajax():
            return render(request,'comment_ajax.html',{'page':page,'page_range':page_range})
        return render(request,'detail.html',{'article':article,'page':page,'page_range':page_range})


def blog_type(request,pk):
    if request.method == 'GET':
        article =  models.Article.objects.filter(article_type__pk = pk)
        paginator = Paginator(article,10)
        page = request.GET.get('page',1)
        page = paginator.get_page(page)
        page_range = range(max(page.number-2,1),min(page.number+2+1,paginator.num_pages+1))

        return render(request,'blog_type.html',{'page':page,'page_range':page_range})


def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username,password=password)
    if user:
        _login(request,user)
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        raise Http404('用户不存在')


def userspace(request,pk):
    user = get_object_or_404(User,pk=pk)
    if request.GET.get('p') == 'article':
        articles = user.article_set.all()
        paginator = Paginator(articles,10)
        page_num = request.GET.get('page',1)
        page = paginator.get_page(page_num)
        page_range = range(max(page.number-2,1),min(page.number+2+1,paginator.num_pages+1))
        return render(request,'aj_user_article.html',{'page':page,'page_range':page_range})
    if not hasattr(user,'avatar'):
        models.Avatar(user=user,path='avatar.jpg').save()
    return render(request,'userspace.html',{'user':user})



def write(request):
    BASE_DIR = os.path.join(settings.MEDIA_ROOT,'user')#所有用户资料公共路径
    if request.user.is_authenticated:
        if request.method == 'POST':
            path = os.path.join(BASE_DIR,str(request.user.pk)) #请求的用户路径
            myFile = request.FILES.get("faceimg",None)
            if not myFile:
                return HttpResponse('无效文件')
            title = request.POST.get('title',None)
            content = request.POST.get('content',None)
            _type = request.POST.get('type',None)
            article_type = get_object_or_404(models.ArticleType,article_type=_type)
            article = models.Article(title=title,article_type=article_type,author=request.user)
            article.save()
            models.Content(article=article,content=content).save()
            ext = os.path.splitext(myFile.name)[1]
            article_path = os.path.join(path,f'{article.pk}')
            if not os.path.exists(article_path):
                os.makedirs(article_path)
            with open(os.path.join(article_path,f'face{ext}'),'wb+') as f:
                for chunk in myFile.chunks():
                    f.write(chunk)
            models.FaceImg(article=article,path=f'user/{request.user.pk}/{article.pk}/face{ext}').save()
            return redirect(reverse('blog:blog_detail',args=(article.pk,)))
        _types = models.ArticleType.objects.all()
        return render(request,'write.html',{'user':request.user,'types':_types})
    return HttpResponse('请登录')