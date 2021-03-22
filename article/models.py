from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField('分类', max_length=100)
    
    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'
        
    def __str__(self):
        return self.name

class Tags(models.Model):
    name = models.CharField('标签', max_length=100)
    
    class Meta:
        verbose_name = '标签'
        verbose_name_plural = "标签"
    
    def __str__(self):
        return self.name
    
class Article(models.Model):
    title = models.CharField('标题', max_length=64)
    content = models.TextField('内容', null=True)
    create_time = models.DateTimeField('发布时间')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='分类', default='1', related_name='articles')
    # 当模型不在同一个app时，设置外键的方式
    author = models.ForeignKey('frontuser.User', on_delete=models.CASCADE, null=True)
    # author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
    tags = models.ManyToManyField(Tags, blank=True)
    # 设置可为空的BooleanField为NullBooleanField
    # removed = models.NullBooleanField()
    # EmailField在数据库层面并不会限制字符串一定要满足邮箱格式，只是以后使用ModalForm等表单相关操作的时候会起作用
    
    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'
    
    def __str__(self):
        # print打印格式
        return '<Article: ({title}, {content}, {create_time})>'.format(title=self.title, content=self.content, create_time=self.create_time)
