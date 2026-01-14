from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from textblob import TextBlob  
from .models import Post, Comment
from django.http import JsonResponse

# 1. HOME PAGE
def home(request):
    return render(request, 'home.html', {
        'my_name': 'Asad', 
        'my_roll': 'B-28015'
    })

# 2. SIGNUP LOGIC (RE-WRITTEN TO WORK)
def signup(request):
    if request.method == "POST":
        uname = request.POST.get('username')
        uemail = request.POST.get('email')
        upass = request.POST.get('password')

        if not uname or not upass:
            messages.error(request, "Please fill all fields!")
            return redirect('signup')

        if User.objects.filter(username=uname).exists():
            messages.error(request, "Username already taken!")
            return redirect('signup')

        # create_user automatically hashes the password
        user = User.objects.create_user(username=uname, email=uemail, password=upass)
        user.save()
        messages.success(request, "Account created! Please login.")
        return redirect('login')
        
    return render(request, 'signup.html')

# 3. LOGIN LOGIC
def login_view(request):
    if request.method == "POST":
        uname = request.POST.get('username')
        upass = request.POST.get('password')

        user = authenticate(username=uname, password=upass)
        if user is not None:
            login(request, user) # Creates Session
            messages.success(request, f"Welcome {uname}!")
            return redirect('home')
        else:
            messages.error(request, "Invalid Details!")
            return redirect('login')

    return render(request, 'login.html')

# 4. LOGOUT
def logout_view(request):
    logout(request)
    return redirect('home')

# 5. STATIC PAGES
def contact(request): return render(request, 'contact.html')
def about(request): return render(request, 'about.html')
def blog_view(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog.html', {'posts': posts, 'my_name': 'Asad', 'my_roll': 'B-28015'})
def post_details_view(request): return render(request, 'post-details.html')
def service(request): return render(request, 'service.html')

# 6. AI SENTIMENT LOGIC
def add_comment(request, post_id):
    if request.method == "POST":
        msg = request.POST.get('message')
        if msg:
            analysis = TextBlob(msg)
            if analysis.sentiment.polarity > 0:
                res = "Positive 😊"
            elif analysis.sentiment.polarity < 0:
                res = "Negative 😠"
            else:
                res = "Neutral 😐"
                
            Comment.objects.create(text=msg, sentiment=res, post_id=post_id)
        return redirect('blog')

# 7. REST API
def post_api(request):
    data = list(Post.objects.values('title', 'content'))
    return JsonResponse(data, safe=False)

# views.py mein update logic
def edit_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if request.method == "POST":
        new_text = request.POST.get('message')
        if new_text:
            comment.text = new_text
            comment.save() # Is se AI sentiment khud hi refresh ho jayega
            messages.success(request, "Comment updated!")
            return redirect('blog')
    
    return render(request, 'edit_comment.html', {'comment': comment})

# views.py mein delete logic
def delete_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    comment.delete()
    messages.success(request, "Comment deleted successfully!")
    return redirect('blog')