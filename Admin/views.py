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
from django.urls import reverse_lazy

# Create your views here.

# ========================================
# AUTHENTICATION VIEWS
# ========================================

def login_view(request):
    """
    Handle user authentication and login process.
    Creates default superuser if it doesn't exist.
    Redirects authenticated users to dashboard.
    """
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


# ========================================

def logout_view(request):
    """
    Handle user logout and redirect to login page.
    """
    logout(request)
    return redirect('login_view')


# ========================================
# DASHBOARD VIEWS
# ========================================
@login_required(login_url=reverse_lazy('error_access_denied'))
def admin_dashboard_view(request):
    """
    Display admin dashboard with statistics and counts.
    Restricted to authenticated superusers only.
    """
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


# ========================================
# BLOG MANAGEMENT VIEWS
# ========================================

@login_required(login_url=reverse_lazy('error_access_denied'))
def post_arena_log_view(request, post_id=None):
    """
    Handle blog post creation and editing.
    Supports both new post creation and existing post updates.
    """
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


# ========================================

@login_required(login_url=reverse_lazy('error_access_denied'))
def manage_blog_view(request):
    """
    Display all blog posts for management.
    Shows posts with author information and categories.
    """
    if not request.user.is_superuser and request.user.username != "admin@admin.com":
        return redirect('error_acces_denied')

    posts = BlogPost.objects.select_related('author').all()
    categories = dict(BlogPost.CATEGORY_CHOICES)
    return render(request, 'Admin/ManageBlogs.html', {'posts': posts, 'categories': categories})


# ========================================

@require_http_methods(["GET", "POST"]) # type: ignore
def delete_post(request, post_id):
    """
    Handle blog post deletion.
    Accepts both GET and POST requests for flexibility.
    """
    try:
        post = get_object_or_404(BlogPost, id=post_id)
        post.delete()
        # Redirect to the blog management page after deletion
        return redirect('manage_blog_view')
    except Exception as e:
        # Handle errors gracefully
        return redirect('manage_blog_view', error="Failed to delete post.")


# ========================================

def blog_detail_view(request, blog_id):
    """
    Display a single blog post in detail with related posts.
    Shows related posts from same category or latest posts if none available.
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


# ========================================

def blog_list_view(request):
    """
    Display all blog posts in a beautiful grid layout.
    Orders posts by creation date (newest first).
    """
    # Get all blog posts ordered by creation date (newest first)
    blogs = BlogPost.objects.all().order_by('-created_at')
    
    context = {
        'blogs': blogs,
    }
    
    return render(request, 'Admin/all_blogs.html', context)


# ========================================
# CONTACT MESSAGE MANAGEMENT VIEWS
# ========================================
@login_required(login_url=reverse_lazy('error_access_denied'))
def contact_messages_view(request):
    """
    Display all contact messages for admin review.
    Shows messages ordered by submission date.
    """
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


# ========================================

def delete_contact_message(request, message_id):
    """
    Handle contact message deletion.
    Restricted to authenticated superusers only.
    """
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


# ========================================
# GALLERY MANAGEMENT VIEWS
# ========================================

@login_required(login_url=reverse_lazy('error_access_denied'))
def manage_gallery_view(request):
    """
    Handle gallery management operations (add, update, delete).
    Supports CRUD operations for gallery items with image uploads.
    """
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add':
            category = request.POST.get('category')
            title = request.POST.get('title')
            gallery_image = request.FILES.get('gallery_image')
            
            if category and gallery_image:
                ManpowerGallery.objects.create(
                    category=category,
                    title=title if title else None,
                    gallery_image=gallery_image
                )
                messages.success(request, 'Gallery item added successfully!')
            else:
                messages.error(request, 'Please select category and upload image.')
        
        elif action == 'update':
            gallery_id = request.POST.get('gallery_id')
            category = request.POST.get('category')
            title = request.POST.get('title')
            gallery_image = request.FILES.get('gallery_image')
            
            try:
                item = ManpowerGallery.objects.get(id=gallery_id)
                item.category = category
                item.title = title if title else None
                
                if gallery_image:
                    item.gallery_image = gallery_image
                
                item.save()
                messages.success(request, 'Gallery item updated successfully!')
            except ManpowerGallery.DoesNotExist:
                messages.error(request, 'Gallery item not found.')
        
        elif action == 'delete':
            gallery_id = request.POST.get('gallery_id')
            
            try:
                item = ManpowerGallery.objects.get(id=gallery_id)
                item.delete()
                messages.success(request, 'Gallery item deleted successfully!')
            except ManpowerGallery.DoesNotExist:
                messages.error(request, 'Gallery item not found.')
        
        return redirect('manage_gallery_view')
    
    # GET request
    gallery_items = ManpowerGallery.objects.all().order_by('-created_at')
    
    return render(request, 'Admin/manage_gallery.html', {
        'gallery_items': gallery_items,
    })


# ========================================
# JOB MANAGEMENT VIEWS
# ========================================

@login_required(login_url=reverse_lazy('error_access_denied'))
def manage_jobs_view(request):
    """
    Handle job management operations (add, update, delete).
    Supports CRUD operations for youth job postings with image uploads.
    """
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add':
            job_title = request.POST.get('job_title')
            category = request.POST.get('category')
            job_image = request.FILES.get('job_image')
            job_description = request.POST.get('job_description')
            
            if job_title and category and job_image and job_description:
                YouthJob.objects.create(
                    job_title=job_title,
                    category=category,
                    job_image=job_image,
                    job_description=job_description
                )
                messages.success(request, 'Job posted successfully!')
            else:
                messages.error(request, 'Please fill in all required fields.')
        
        elif action == 'update':
            job_id = request.POST.get('job_id')
            job_title = request.POST.get('job_title')
            category = request.POST.get('category')
            job_image = request.FILES.get('job_image')
            job_description = request.POST.get('job_description')
            
            try:
                job = YouthJob.objects.get(id=job_id)
                job.job_title = job_title
                job.category = category
                job.job_description = job_description
                
                if job_image:
                    job.job_image = job_image
                
                job.save()
                messages.success(request, 'Job updated successfully!')
            except YouthJob.DoesNotExist:
                messages.error(request, 'Job not found.')
        
        elif action == 'delete':
            job_id = request.POST.get('job_id')
            
            try:
                job = YouthJob.objects.get(id=job_id)
                job.delete()
                messages.success(request, 'Job deleted successfully!')
            except YouthJob.DoesNotExist:
                messages.error(request, 'Job not found.')
        
        return redirect('manage_jobs_view')
    
    # GET request
    jobs = YouthJob.objects.all().order_by('-posted_at')
    
    return render(request, 'Admin/manage_jobs.html', {
        'jobs': jobs,
    })

# ========================================
# END OF VIEWS
# ========================================