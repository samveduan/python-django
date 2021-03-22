#--*--encoding--*--
from django.shortcuts import render
from django.http import HttpResponse
from .models import Article, Category
from frontuser.models import User
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone #引入timezone模块
import datetime
import csv
from django.http import StreamingHttpResponse

# Create your views here.
class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)

def index(request):
    return render(request, 'article.html')

# 获取所有                                                                                                                                                                                                                                          
@csrf_exempt
def all(request):
    if request.method == 'GET':
        pageSize = int(request.GET.get('pageSize'))
        pageNumber = int(request.GET.get('pageNumber'))
        searchText = request.GET.get('searchText')
        sortName = request.GET.get('sortName')
        sortOrder = request.GET.get('sortOrder')
    
    total = Article.objects.all().count()
    articles = Article.objects.order_by('-id')[(pageNumber-1)*pageSize:(pageNumber)*pageSize]
    print(articles)
    rows = []
    data = {"total": total, "rows": rows}
    for article in articles:
        rows.append({'id': article.id, 'title': article.title, 'content': article.content, 'create_time': article.create_time})
        
    return HttpResponse(json.dumps(data, cls=CJsonEncoder), content_type="application/json")

# 增加
@csrf_exempt
def add(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        article = Article(title = title, content = content, create_time = timezone.now())
        r = article.save()
        ret = {"ret": True, 'title': title, 'content': content, 'r': r}
        return HttpResponse(json.dumps(ret))

def article(request, article_id):
    article = Article.objects.get(pk = article_id)
    return render(request, 'article.html', {'article': article})

# 删除
@csrf_exempt
def delete(request):
    return_dict = {"ret": True, "errMsg": "", "rows": []}
    article_ids = request.POST.getlist('ids')
    for id in article_ids:
        #Article.objects.filter(id=int(id)).delete()
        Article.objects.get(pk=int(id)).delete()
    return HttpResponse(json.dumps(return_dict))

# 编辑
@csrf_exempt
def edit(request):
    return_dict = {"ret": True, "errMsg": "", "msg": ''}
    if request.method == 'POST':
        id = request.POST.get('id')
        title = request.POST.get('title')
        content = request.POST.get('content')
        article = Article.objects.get(pk=id)
        article.title = title
        article.content = content
        article.save()
        return_dict['msg'] = '修改成功'

    return HttpResponse(json.dumps(return_dict), content_type="application/json")

# 获取单条数据
@csrf_exempt
def get_a_article(request):
    return_dict = {"ret": True, "errMsg": "", "title": '', 'content': '', 'id': ''}
    
    if request.method == 'POST':
        id = request.POST.get('id')
        #pk => primary key
        article = Article.objects.filter(pk=id)[0].__dict__
        return_dict['title'] = article['title']
        return_dict['content'] = article['content']
        return_dict['id'] = article['id']
        
    return HttpResponse(json.dumps(return_dict), content_type="application/json")
        
def orm(request):
    all = Article.objects.all()
    print(type(all))
    print(all)
    return HttpResponse('orm')

def open_a_article(request, article_id):
    # filter方法返回的是一个'QuerySet'对象，这个对象类似于一个列表
    article = Article.objects.filter(id=article_id).first()
    return render(request, 'article.html', {'article': article})

# 添加外键    
def foreign(request):
    #category = Category(name='科技')
    #category.save()
    #category = Category.objects.get(pk=1)
    #article = Article(title='1', content='2', create_time = timezone.now())
    #article.category = category
    #article.save()
    
    #获取category
    article = Article.objects.first()
    print(article.category.name)
    return HttpResponse("外键关联成功！")

def one_to_many(request):
    # 一对多的关联操作
    # user = User(username='吴承恩')
    # user.save()
    # category = Category.objects.first()
    # article = Article(title='西游记', content="555", create_time=timezone.now())
    # article.category = category
    # article.author = user
    # article.save()
    # return HttpResponse("外键关联成功！")

    # 获取某个分类下的第一条数据
    # category = Category.objects.first()
    # article = category.article_set.first()
    # print(article)
    # return HttpResponse("success")

    # 获取某个分类下的所有数据
    # category = Category.objects.first()
    # articles = category.article_set.all()
    # articles = category.articles.all()
    #print(articles)
    # for x in articles:
        # print(x.title)
    # return HttpResponse("success")
    
    # 添加关联数据的其它方式
    category = Category.objects.first()
    article = Article(title='水浒传', content='宋江......', create_time = timezone.now())
    article.author = User.objects.first()
    category.articles.add(article, bulk=False)
    return HttpResponse('success')
    
def query(request):
     # 在windows操作系统上，MySql排序规则(Collation)无论是什么大小写都不敏感
     # 在Linux操作系统上，MySql排序规则(Collation)是utf8_bin，name大小写敏感
     # article = Article.objects.filter(id__exact=4)
     
     # Like和=，大多数情况下是等价的，只有少数情况下是不等价的，'like %搜索词%'就是模糊匹配,'like 搜索词' <=>'= 搜索词'
     # exact和iexact的区别就是'LIKE'和'='的区别，因为exact在底层会翻译成'='，iexact会翻译成'LIKE'
     # filter返回的是一个QuerySet
     # article = Article.objects.filter(id__iexact=4)
     
     # get返回的是一个ORM模型
     # article = Article.objects.get(id__iexact=4)
     
     
     # contains：使用大小写敏感的判断，某个字符串是否在指定的字段中，在使用的时候会被翻译成'like binary'
     # icontains:使用大小写不敏感的判断，某个字符串是否在指定的字段中，在使用的时候会被翻译成'like'，而'like'在MySQL中是不区分大小写的
     # contains、icontains和iexact的区别：
     # contains、icontains在被翻译成SQL的时候使用的是'%value%'，就是整个字符串中只要出现了'value'都能够被找到；而'iexact'没有百分号，那么意味着只有完全相等的时候才会被匹配
     result = Article.objects.filter(title__contains='钢铁')
     
     print(type(result))
     # QuerySet.query将ORM查询语句转换为sql语句,但query只能在QuerySet上使用，不能在ORM模型上使用
     print(result.query)
     return HttpResponse('success')
 
def test(request):
     result = Article.objects.filter(pk=6)
     print(type(result))
     return HttpResponse('success')

class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value

@csrf_exempt
def download(request):
    """A view that streams a large CSV file."""
    # Generate a sequence of rows. The range is based on the maximum number of
    # rows that can be handled by a single sheet in most spreadsheet
    # applications.
    rows = (["Row {}".format(idx), str(idx)] for idx in range(65536))
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse((writer.writerow(row) for row in rows), content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
    return response

@csrf_exempt
def download_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

    writer = csv.writer(response)
    writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
    writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])

    return response
    
@csrf_exempt
def get_data(request):
    return_dict = {"ret": True, "framework": "React"}
        
    return HttpResponse(json.dumps(return_dict), content_type="application/json")

@csrf_exempt
def check_login_status(request):
    return_dict = {"ret": False}
 
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == 'admin' and password == '123456':
            return_dict['ret'] = True
 
    return HttpResponse(json.dumps(return_dict), content_type="application/json")

@csrf_exempt
def get_table_data(request):
    return_dict = {"ret": False}
 
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        print(username)
        print(password)

        if username == 'admin' and password == '123456':
            return_dict['ret'] = True
 
    return HttpResponse(json.dumps(return_dict), content_type="application/json")

@csrf_exempt
def test_axios(request):
    return_dict = {"ret": False, "name": "axios"}
 
    if request.method == "POST":
        return_dict['ret'] = True
 
    return HttpResponse(json.dumps(return_dict), content_type="application/json")