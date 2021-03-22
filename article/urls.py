"""articles URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, re_path
from . import views

urlpatterns = [
    path('index/', views.index),
    path('all/', views.all),
    path('add/', views.add),
    re_path('^article/(?P<article_id>[0-9]+)/$', views.open_a_article, name='article_page'),
    path('get_a_article/', views.get_a_article),
    path('edit/', views.edit),
    path('delete/', views.delete),
    path('orm/', views.orm),
    path('foreign/', views.foreign),
    path('one_to_many/', views.one_to_many),
    path('query/', views.query),
    path('test/', views.test),
    path('download/', views.download),
    path('get_data/', views.get_data),
    path('check_login_status/', views.check_login_status),
    path('test_axios/', views.test_axios),
]
