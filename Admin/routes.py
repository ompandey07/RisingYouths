from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views 

urlpatterns = [
    

    path('arena/', views.post_arena_log_view , name="post_arena_log_view"),
    path('edit-blog/<int:post_id>/', views.post_arena_log_view, name='edit_blog'),
    path('manage_arena/', views.manage_blog_view , name="manage_blog_view"),
    path('delete-post/<int:post_id>/', views.delete_post, name='delete_post'),


    path('login/', views.login_view, name='login_view'),
    path('admin_dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
 
    
    
]

# Serve static and media files during development (when DEBUG is True)
if settings.DEBUG:
    # Serve media files
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Serve static files
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)