from django.contrib import admin
from .models import Article, Category, Tags

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'create_time', )
    list_display_links = ('id', 'title')
    search_fields=['title']
    date_hierarchy = 'create_time'    # 详细时间分层筛选　
    
# Register your models here.
admin.site.register(Article, ArticleAdmin)
admin.site.register(Category)
admin.site.register(Tags)

#admin.site.site_header = 'Django中文网管理后台'
#admin.site.site_title = 'Django中文网'

#list_editable 设置默认可编辑字段，在列表里就可以编辑
list_editable = ['title']