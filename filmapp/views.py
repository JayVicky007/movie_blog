from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Blog
from .forms import BlogForm, RegistrationForm, ContactForm
from django.core.paginator import Paginator


def home(request):
    # Retrieve all blog posts
    all_blogs = Blog.objects.all().order_by('-created_at')

    # Set the number of blog posts to display per page
    blogs_per_page = 3

    # Create a Paginator instance
    paginator = Paginator(all_blogs, blogs_per_page)

    # Get the current page number from the request's GET parameters
    page_number = request.GET.get('page')

    # Get the Page object for the current page
    page = paginator.get_page(page_number)

    return render(request, 'filmapp/home.html', {'page': page})

def admin_posts(request):
    # Retrieve all blog posts
    admin_blogs = Blog.objects.filter(author__is_superuser=True).order_by('-created_at')

    # Set the number of blog posts to display per page
    blogs_per_page = 3

    # Create a Paginator instance
    paginator = Paginator(admin_blogs, blogs_per_page)

    # Get the current page number from the request's GET parameters
    page_number = request.GET.get('page')

    # Get the Page object for the current page
    page = paginator.get_page(page_number)

    return render(request, 'filmapp/admin_posts.html', {'page': page})



def guest_reviews(request):
    guest_posts = Blog.objects.filter(author__is_superuser=False).order_by('-created_at')

    blogs_per_page = 3

    paginator = Paginator(guest_posts, blogs_per_page)

    page_number = request.GET.get('page')

    page = paginator.get_page(page_number)

    return render(request, 'filmapp/guest_reviews.html', {'page': page})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():  # Correct the condition here
            form.save()  # Save the form data to the database
            return redirect("filmapp:login")  # Redirect to a success page or URL

    else:
        form = ContactForm()

    return render(request, 'filmapp/contact.html', {'form': form})

@login_required(login_url='filmapp:login')  # Add this decorator to require authentication.
def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)  # Include request.FILES for file uploads
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user  # Assign the logged in user as the author
            blog.save()
            return redirect('filmapp:home')
    else:
        form = BlogForm()
    
    return render(request, 'filmapp/create_blog.html', {'form': form})


def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('filmapp:login')
    return render(request, 'filmapp/auth/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('filmapp:home') 
    else:
        form = AuthenticationForm()
    
    return render(request, 'filmapp/auth/login.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('filmapp:login')

def blog_detail(request, pk):
    blog = Blog.objects.get(pk=pk)
    return render(request, "filmapp/blog_detail.html", {"blog": blog})

def search(request):
    query = request.GET.get('q')  # Get the search query from the request's GET parameters
    results = []

    if query:
        # Perform a search query using your model's fields
        results = Blog.objects.filter(title__icontains=query)  # Example: Search in the 'title' field

    return render(request, 'filmapp/search_results.html', {'query': query, 'results': results})

def author_posts(request, author_id):
    author = get_object_or_404(User, id=author_id)  # Retrieve the author by their User ID
    author_posts = Blog.objects.filter(author=author)

    return render(request, 'filmapp/author_posts.html', {'author': author, 'author_posts': author_posts})


import requests
from bs4 import BeautifulSoup

def trending(request):
    url = 'https://www.rottentomatoes.com/browse/tv_series_browse/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    series_list_div = soup.find('div', class_='discovery-tiles__wrap')

    titles = []
    images = []
    audience_scores = []

    for series_div in series_list_div.find_all('div', class_='js-tile-link'):
        title = series_div.find('span', {'class': 'p--small', 'data-qa': 'discovery-media-list-item-title'}).text.strip()
        titles.append(title)

        image_url = series_div.find('img', class_='posterImage')['src']
        images.append(image_url)

        audience_score_elem = series_div.find('score-pairs', {'audiencescore': True})
        if audience_score_elem:
            audience_score_str = audience_score_elem['audiencescore']
            audience_score = int(audience_score_str)
            
            if 70 <= audience_score <= 100:
                audience_scores.append(audience_score)

    audience_scores.sort(reverse=True)

    series_data = zip(titles, images, audience_scores)

    return render(request, 'filmapp/trending.html', {
        'series_data': series_data
    })



