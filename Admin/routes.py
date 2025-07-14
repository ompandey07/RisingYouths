from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views 

urlpatterns = [
    

    path('arena/', views.post_arena_log_view , name="post_arena_log_view"),
    path('edit-blog/<int:post_id>/', views.post_arena_log_view, name='edit_blog'),
    path('manage_blogs/', views.manage_blog_view , name="manage_blog_view"),
    path('delete-post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('blog/<int:blog_id>/', views.blog_detail_view, name='blog_detail'),
    path('blogs/', views.blog_list_view, name='blog_list'),


    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('dashboard/', views.admin_dashboard_view, name='admin_dashboard'),



    path('contact_messages/', views.contact_messages_view, name='contact_messages_view'),
    path('delete_contact_message/<int:message_id>/', views.delete_contact_message, name='delete_contact_message'),


    path('gallery/', views.manage_gallery_view, name='manage_gallery_view'),


    path('jobs/', views.manage_jobs_view, name='manage_jobs_view'),
 
    
    
]

# Serve static and media files during development (when DEBUG is True)
if settings.DEBUG:
    # Serve media files
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Serve static files
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)