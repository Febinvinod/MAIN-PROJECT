from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
        # path('regform/',views.userRegister,name='regform'),
        path('blogs/',views.blog,name='blogs'),
        path('blogcategory/<int:catid>',views.catblog,name='blogcategory'),
        path('single_blog/<int:post_id>/',views.single_blog,name='single_blog'),
        path('add_blog/',views.add_blog,name='add_blog'),
        path('view_blog_editor/',views.view_blog_editor,name='view_blog_editor'),
        path('single_view_editor/<int:post_id>/',views.single_view_editor,name='single_view_editor'),
        path('post_status/<int:post_id>/',views.post_status,name='post_status'),
        path('edit_blog/<int:post_id>/',views.edit_blog,name='edit_blog'),
        path('delete_blog/<int:post_id>/',views.delete_blog,name='delete_blog'),


        # path('update_post/<int:post_id>/', views.update_post, name='update_post'),




]  
