from django.urls import path, include
from .import views  
from .feeds import LatestPostsFeed
from django.conf.urls import url
from .views import addpost
from django.contrib import admin


app_name ='blog'

urlpatterns = [
    # post views
    path('post_list', views.post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',views.post_detail,name='post_detail'),
   
]
urlpatterns = [
    # post views
    path('', views.post_list, name='post_list'),
    #path('', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',views.post_detail,name='post_detail'),
    path('post/new/',views.addpost,name='post'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/edit',views.post_edit,name='post_edit'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/delete/', views.post_delete, name='post_delete'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/deleted/', views.post_deleted, name='post_deleted'),
    path ('<int:post_id>/share/', views.post_share, name= 'post_share'),
    path('tag/<slug:tag_slug>/',views.post_list, name='post_list_by_tag'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('blogs/', views.blogs, name='blogs'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('post/', views.addpost, name='post'),
   
]
