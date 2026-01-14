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
def blog_view(request): return render(request, 'blog.html')
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
        return redirect('post_details')

# 7. REST API
def post_api(request):
    data = list(Post.objects.values('title', 'content'))
    return JsonResponse(data, safe=False)

from django.contrib import admin
from .models import Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Yeh columns Admin ki list mein nazar ayenge
    list_display = ('title', 'author', 'created_at')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    # Yeh confirm karega ke Sentiment field samne nazar aa rahi hai
    list_display = ('text', 'sentiment', 'post')