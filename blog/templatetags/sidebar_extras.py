from django import template
from django.utils.html import mark_safe,format_html
from blog.models import Article
from django.shortcuts import reverse
register = template.Library()

@register.simple_tag
def sidebar():
    arls =  Article.objects.all()[0:5]
    html = ''
    for each in arls:
        html = html + f'<p><a href="{reverse("blog:blog_detail",args=(each.pk,))}">{each.title}</a></p>'
    html = '<div class="sidebar">' + '<h3>热门文章</h3>' + html + '</div>'
    return mark_safe(html)