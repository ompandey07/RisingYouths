from django.shortcuts import render , redirect
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .models import BlogPost
from django.contrib.auth.models import User

# Create your views here.





def login_view(request):
    # Create default user if it doesn't exist
    default_username = "risingyouth@admin.com"
    default_password = "admin@1200"
    
    if not User.objects.filter(username=default_username).exists():
        User.objects.create_superuser(
            username=default_username, 
            email=default_username, 
            password=default_password
        )
        print(f"Default superuser created: {default_username}")
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin_dashboard')  # Redirect to the admin dashboard after login
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'Admin/login.html')




def admin_dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login_view')  # Redirect to login if not authenticated

    if not request.user.is_superuser and request.user.username != "admin@admin.com":
        return redirect('error_acces_denied')

    return render(request, 'Admin/AdminDashboard.html')







@login_required
def post_arena_log_view(request, post_id=None):
    if not request.user.is_superuser and request.user.username != "admin@admin.com":
        return redirect('error_acces_denied')

    post = None  # Initialize post as None in case it's not found

    if post_id:
        # Check if post_id is provided (for editing)
        post = get_object_or_404(BlogPost, id=post_id)

    if request.method == 'POST':
        try:
            # Extract form data
            title = request.POST.get('title')
            content = request.POST.get('description')
            category = request.POST.get('category')
            new_image = request.FILES.get('imageInput')

            # Validate required fields
            if not all([title, category]):
                messages.error(request, 'Title and category are required')
                return render(request, 'Admin/PublishBlog.html', {
                    'categories': BlogPost.CATEGORY_CHOICES,
                    'post': post  # Pass post to the template for editing
                })

            if post:
                # Update existing post
                post.title = title
                post.content = content
                post.category = category.upper()
                if new_image:
                    post.image = new_image
                post.save()
                return render(request, 'Admin/PublishBlog.html', {
                    'categories': BlogPost.CATEGORY_CHOICES,
                    'post': post,
                    'success_message': 'Blog post updated successfully!',
                    'is_published': False
                })
            else:
                # Create new post
                BlogPost.objects.create(
                    title=title,
                    content=content,
                    category=category.upper(),
                    image=new_image if new_image else None,
                    author=request.user
                )
                return render(request, 'Admin/PublishBlog.html', {
                    'categories': BlogPost.CATEGORY_CHOICES,
                    'success_message': 'Blog post published successfully!',
                    'is_published': True
                })

        except Exception as e:
            messages.error(request, f'Error with blog post: {str(e)}')

    return render(request, 'Admin/PublishBlog.html', {
        'categories': BlogPost.CATEGORY_CHOICES,
        'post': post  # Pass post to the template for editing if it's provided
    })




#? -------------------------------------------------------------------------------------------------------------------------------------------------------

# View for manage blog posts
@login_required
def manage_blog_view(request):
    if not request.user.is_superuser and request.user.username != "admin@admin.com":
        return redirect('error_acces_denied')

    posts = BlogPost.objects.select_related('author').all()
    categories = dict(BlogPost.CATEGORY_CHOICES)
    return render(request, 'Admin/ManageBlogs.html', {'posts': posts, 'categories': categories})




#? -------------------------------------------------------------------------------------------------------------------------------------------------------

# View for delete blog posts
@require_http_methods(["GET", "POST"]) # type: ignore
def delete_post(request, post_id):
    try:
        post = get_object_or_404(BlogPost, id=post_id)
        post.delete()
        # Redirect to the blog management page after deletion
        return redirect('manage_blog_view')
    except Exception as e:
        # Handle errors gracefully
        return redirect('manage_blog_view', error="Failed to delete post.")