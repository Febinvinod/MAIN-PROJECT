from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from .models import Posts,BlogCategory,PostView,Comment
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from home.models import UserProfile

def blog(request):
    # Retrieve all published posts
    posts = Posts.objects.filter(is_published=True, is_active =True)
    cat = BlogCategory.objects.all()
    # print(list(posts))
    return render(request, 'blog.html', {'posts': posts, 'cat': cat})
@login_required
def catblog(request,catid):
    # Retrieve all published posts
    cat = BlogCategory.objects.get(pk= catid)
    posts = Posts.objects.filter(is_published=True, is_active =True, category=cat)
    # print(list(posts))
    return render(request, 'blog.html', {'posts': posts})

@login_required
def view_blog_editor(request):
    # Retrieve all published posts
    posts = Posts.objects.filter(author=request.user,is_active =True)
    # print(list(posts))
    return render(request, 'lists-blog-editors.html', {'posts': posts})

@login_required
def single_blog(request, post_id):
    # Retrieve single post by its id
    post = get_object_or_404(Posts, pk=post_id)
    cat = BlogCategory.objects.all()
    cuser = request.user

    # Update or create a PostView object to track post views
    try:
        cpost = PostView.objects.get(user=cuser, post=post)
    except PostView.DoesNotExist:
        cpost = None

    if not cpost:
        PostView.objects.create(user=cuser, post=post)
        post.total_views += 1
        post.save() 

    # Handle comment submission
    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        if comment_text:  # Ensure comment_text is not empty before creating a comment
            userprofile = UserProfile.objects.get(user=cuser)
            new_comment = Comment.objects.create(
                post=post,
                comment_author=userprofile,  # Assuming author is a UserProfile object
                content=comment_text
            )
            return redirect('single_blog', post_id=post_id)

    # Fetch all posts for rendering in the sidebar (assuming it's for navigation)
    posts = Posts.objects.filter(is_published=True,is_active=True)

    # Fetch comments for the current post
    comments = Comment.objects.filter(post=post)
    count = comments.count()  # Count the number of comments


    return render(request, 'detail.html', {'post': post, 'posts': posts, 'cat': cat, 'comments': comments, 'count': count})

@login_required
def add_blog(request):
    
    cuser=request.user
    
    if request.method == 'POST':
        # Retrieve data from the form submission
        title = request.POST.get('title')
        subtitle1 = request.POST.get('subtitle1')
        subtitle2 = request.POST.get('subtitle2')
        subtitle3 = request.POST.get('subtitle3')
        subtitle = request.POST.get('subtitle')
        intro = request.POST.get('intro')
        content1 = request.POST.get('content1')
        content2 = request.POST.get('content2')
        content3 = request.POST.get('content3')
        image = request.FILES.get('image')
        category = request.POST.get('category')
        
        current_category = BlogCategory.objects.get(name=category)
        print(current_category)
        category_id = current_category.id
        print(category_id)
          # Assuming category is submitted as ID
        # Create a new Posts object with the retrieved data
        post = Posts.objects.create(
            title=title,
            subtitle1=subtitle1,
            subtitle2=subtitle2,
            subtitle3=subtitle3,
            subtitle=subtitle,
            intro=intro,
            content1=content1,
            content2=content2,
            content3=content3,
            image=image,
            category_id=category_id,
            author=cuser
        )
        # Optionally, you can do additional processing or redirect the user to another page
        return redirect('view_blog_editor')  # Redirect to home page after successfully adding the post
    else:
        cat = BlogCategory.objects.all()

        # Handle GET request (render the form)
        return render(request, 'newblog.html',{'cat':cat})

@login_required
def single_view_editor(request, post_id):
    # Retrieve single post by its id
    post = get_object_or_404(Posts, pk=post_id)
    cat = BlogCategory.objects.all()
    cuser = request.user

    # Retrieve all published posts
    posts = Posts.objects.filter(is_published=True)
    return render(request, 'singleview.html', {'post': post})


def post_status(request, post_id):
    try:
        # Retrieve single post by its id
        post = get_object_or_404(Posts, pk=post_id)
        # Set is_published to True
        post.is_published = True
        post.status = Posts.PUBLISHED
        post.save()
    except Posts.DoesNotExist:
        # Handle the case where the post does not exist
        return redirect('view_blog_editor')  # Redirect to an error page or return an appropriate response
    
    # Redirect to view_blog_editor after updating the post status
    return redirect('view_blog_editor')



@login_required
def edit_blog(request,post_id):
    
    if request.method == 'POST':
        # Retrieve the post object or return a 404 error if not found
        post = get_object_or_404(Posts, pk=post_id)
        
        # Get the data from the request
        title = request.POST.get('title')
        subtitle1 = request.POST.get('subtitle1')
        subtitle2 = request.POST.get('subtitle2')
        subtitle3 = request.POST.get('subtitle3')
        subtitle = request.POST.get('subtitle')
        intro = request.POST.get('intro')
        content1 = request.POST.get('content1')
        content2 = request.POST.get('content2')
        content3 = request.POST.get('content3')
        image = request.FILES.get('image')

        # Check if each field is provided and update the post accordingly
        if title:
            post.title = title
        if subtitle1:
            post.subtitle1 = subtitle1
        if subtitle2:
            post.subtitle2 = subtitle2
        if subtitle3:
            post.subtitle3 = subtitle3
        if subtitle:
            post.subtitle = subtitle
        if intro:
            post.intro = intro
        if content1:
            post.content1 = content1
        if content2:
            post.content2 = content2
        if content3:
            post.content3 = content3
        if image:
            post.image = image

        
        post.save()
        #messages.success(request, 'Blog edited successfully!')
        # Optionally, you can do additional processing or redirect the user to another page
        return redirect('view_blog_editor')  # Redirect to home page after successfully adding the post
    else:
        post = get_object_or_404(Posts, pk=post_id)

        # Handle GET request (render the form)
    return render(request, 'edit-blog.html',{'post':post})


@login_required
def delete_blog(request, post_id):
    # Retrieve single post by its id
    post = get_object_or_404(Posts, pk=post_id)
    if post:
        post.is_active = False
        post.save()
        #messages.success(request, 'Blog Deleted Successfully!')
    return redirect('view_blog_editor')
    

# ----------------------------------------------------------
# COMMENTS
# ----------------------------------------------------------

@login_required
def add_comments(request, post_id):
    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        post = get_object_or_404(Posts, pk=post_id)

        new_comment = Comment.objects.create(
            post=post,
            author=request.user,
            content=comment_text
        )

        return redirect('single_blog', post_id=post_id)
    else:
        # Handle GET request
        return redirect('single_blog', post_id=post_id)
    