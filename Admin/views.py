from django.shortcuts import render , redirect
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .models import BlogPost , YouthJob, ManpowerGallery
from Backend.models import ContactMessage
from django.contrib.auth.models import User
from django.db.models import Count

# Create your views here.





def login_view(request):
    # If user is already authenticated, redirect to dashboard
    if request.user.is_authenticated:
        return redirect('admin_dashboard')

    # Create default user if it doesn't exist
    default_email = "risingyouth@admin.com"
    default_password = "admin@1200"

    if not User.objects.filter(email=default_email).exists():
        User.objects.create_superuser(
            username=default_email,  # Using email as username
            email=default_email,
            password=default_password
        )
        print(f"Default superuser created: {default_email}")

    if request.method == 'POST':
        email = request.POST.get('username')  # Input field is named 'username' but contains email
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'Invalid email or password')
        except User.DoesNotExist:
            messages.error(request, 'Invalid email or password')

    return render(request, 'Admin/login.html')


def logout_view(request):
    logout(request)
    return redirect('login_view')




def admin_dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login_view')

    if not request.user.is_superuser and request.user.username != "admin@admin.com":
        return redirect('error_acces_denied')

    # Real data counts
    total_blogs = BlogPost.objects.count()
    total_contact = ContactMessage.objects.count()
    total_jobs = YouthJob.objects.count()  # Add this
    total_gallery_images = ManpowerGallery.objects.count()  # Add this

    context = {
        'total_blogs': total_blogs,
        'total_contact': total_contact,
        'total_jobs': total_jobs,  # Add this
        'total_gallery_images': total_gallery_images,  # Add this
    }

    return render(request, 'Admin/AdminDashboard.html', context)







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
    



def blog_detail_view(request, blog_id):
    """
    Display a single blog post in detail with related posts.
    """
    # Get the specific blog post or return 404 if not found
    blog = get_object_or_404(BlogPost, id=blog_id)
    
    # Get related posts (same category, excluding current post)
    related_blogs = BlogPost.objects.filter(
        category=blog.category
    ).exclude(id=blog_id).order_by('-created_at')[:3]
    
    # If no related posts in same category, get latest posts
    if not related_blogs:
        related_blogs = BlogPost.objects.exclude(
            id=blog_id
        ).order_by('-created_at')[:3]
    
    context = {
        'blog': blog,
        'related_blogs': related_blogs,
    }
    
    return render(request, 'Admin/blog_detail.html', context)



def blog_list_view(request):
    """
    Display all blog posts in a beautiful grid layout.
    """
    # Get all blog posts ordered by creation date (newest first)
    blogs = BlogPost.objects.all().order_by('-created_at')
    
    
    context = {
        'blogs': blogs,
    }
    
    return render(request, 'Admin/all_blogs.html', context)





def contact_messages_view(request):
    if not request.user.is_authenticated:
        return redirect('login_view')
    
    if not request.user.is_superuser and request.user.username != "admin@admin.com":
        return redirect('error_acces_denied')
    
    # Latest messages at end (remove '-' from ordering)
    contact_messages = ContactMessage.objects.all().order_by('submitted_at')
    total_messages = contact_messages.count()
    
    context = {
        'contact_messages': contact_messages,
        'total_messages': total_messages,
    }
    
    return render(request, 'Admin/ContactMessages.html', context)


def delete_contact_message(request, message_id):
    if not request.user.is_authenticated:
        return redirect('login_view')
    
    if not request.user.is_superuser and request.user.username != "admin@admin.com":
        return redirect('error_acces_denied')
    
    if request.method == 'POST':
        try:
            message = ContactMessage.objects.get(id=message_id)
            message.delete()
            messages.success(request, 'Contact message deleted successfully!')
        except ContactMessage.DoesNotExist:
            messages.error(request, 'Message not found!')
    
    return redirect('contact_messages_view')

