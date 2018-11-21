from django.shortcuts import render,get_object_or_404,HttpResponse
from .models import Articles
from django.views.generic import RedirectView,View
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from .forms import EmailForm,CommentForm
from django.core.mail import send_mail
from django.conf import settings
from haystack.views import SearchView
from django.db.models import Q
import redis
from django.conf import settings
from django.views.decorators.http import require_http_methods

r=redis.StrictRedis(host=settings.REDIS_HOST,
                    port=settings.REDIS_PORT,
                    db=settings.REDIS_DB)
# Create your views here.


class ArticleList(View):
    # model = Articles
    # context_object_name = 'articles'
    # paginate_by = 1
    # template_name = 'mysite/articleList.html'
    def get(self,request):
        articles = Articles.objects.filter(user=request.user)
        pages = Paginator(articles, 5)
        page1=request.GET.get('page',None)
        try:
            page = pages.page(page1)
        except PageNotAnInteger:
            page = pages.page(1)
        except EmptyPage:
            page = pages.page(pages.num_pages)
        return render(request, 'mysite/articleList.html', locals())

@require_http_methods(['GET','POST'])
def ArticleDetial(request,slug):
    if request.method=='GET':
        article=get_object_or_404(Articles,slug=slug)
        comments=article.comment_set.filter(active=True)
        forms=CommentForm()

        article_tags=article.tags.values_list('id',flat=True)
        similar_articles=Articles.objects.filter(tags__in=article_tags).exclude(id=article.id)

        #????
        key='views:{}'.format(article.slug)
        vv = request.session.get(key, '')
        if not vv:
            '''???????views'''
            request.session[key] = str(request.user)
            request.session.set_expiry(0)  # ??????????
            total_views = r.incr('arricle:{}:views'.format(article.id))  # ??????1

        total_views = int(r.get('arricle:{}:views'.format(article.id)))
        r.zincrby('article_ranking', article.id, 1)
        article_ranking = r.zrange('article_ranking', 0, -1, desc=True)[:5]
        article_ranking_ids = [int(id) for id in article_ranking]
        most_viewed = list(Articles.objects.filter(id__in=article_ranking_ids))
        most_viewed.sort(key=lambda x: article_ranking_ids.index(x.id))

        return render(request,'mysite/articleDetial.html',locals())
    else:
        forms=CommentForm(request.POST)
        article = get_object_or_404(Articles, slug=slug)
        comments = article.comment_set.filter(active=True)
        if forms.is_valid():
            new_comm=forms.save(commit=False)
            new_comm.article=article
            new_comm.save()
            msg='????'
            return render(request, 'mysite/articleDetial.html', locals())

class article_share(View):
    def get(self,request,pk):
        article=get_object_or_404(Articles,id=pk)
        form=EmailForm()
        return render(request,'mysite/share.html',locals())

    def post(self,request,pk):
        article=get_object_or_404(Articles,id=pk)
        form=EmailForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            article_url='https://127.0.0.1:8000/mysite/article/'+article.slug
            subject='{} recommendss you reading?'.format(article.title)
            message='Read {} at {}'.format(article.title,article_url)
            send_mail(subject,message,settings.DEFAULT_EMAIL_FROM,[cd['to']])
            return render(request, 'mysite/share.html', locals())

#??
#??????????????
#??????????
class MySeachView(SearchView):
    template = 'search/search.html'

    def extra_context(self):       #??extra_context??????context??
        context = super(MySeachView,self).extra_context()
        a=self.form.cleaned_data['q']
        articles = Articles.objects.filter(Q(title__icontains=a)|Q(content__icontains=a)).order_by('created_time')[:8]
        context['articles'] = articles
        return context

def govote(request,pk):
    if request.method=='GET' and request.is_ajax():
        try:
            article=Articles.objects.get(id=pk)
            article.like=article.like+1
            article.save()
            like=article.like
        except:
            like=0
    else:
        like=0
    return HttpResponse(like)