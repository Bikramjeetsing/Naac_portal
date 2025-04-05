from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.urls import reverse 
from home.models import Year, Chapter, SubChapter, Category, PDF
from datetime import datetime
from django.http import JsonResponse



# ✅ Home page (with login form)

def home(request):
    # Get all available years
    years = Year.objects.all()

    if not years:
        return render(request, 'alert.html', {'message': 'No years available.'})

    context = {
        'years': years,
    }
    return render(request, 'index.html', context)

# ✅ Chapter page
def chapter(request):
    year = request.GET.get('year')
    
    # Filter by year if provided, else return all chapters
    if year:
        chapters = Chapter.objects.filter(year__year=year).prefetch_related(
            'subchapters__categories'
        )
        
        # Handle case where no chapters are found for a given year
        if not chapters.exists():
            return render(request, 'chapters.html', {
                'chapters': chapters,
                'message': f"No chapters found for year {year}."
            })
    else:
        chapters = Chapter.objects.prefetch_related('subchapters__categories').all()

    return render(request, 'chapters.html', {'chapters': chapters})

# ✅ Alert view
def alert_view(request):
    return render(request, "alert.html")

# ✅ Login view (with better handling and cleaner code)
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import render, redirect

User = get_user_model()  # Get the User model

def login_view(request):
    errors = {'username': '', 'password': ''}  # Dictionary to store errors

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if fields are empty
        if not username:
            errors['username'] = 'Username is required.'
        if not password:
            errors['password'] = 'Password is required.'

        if username and password:  # Proceed only if both fields are filled
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('home')
            else:
                # Check if the username exists in the database
                if not User.objects.filter(username=username).exists():
                    errors['username'] = 'Username not found.'
                else:
                    errors['password'] = 'Incorrect password.'

    return render(request, 'login.html', {'errors': errors})


# ✅ File Upload Page
def File_upload(request):
    years = Year.objects.all()
    chapters = Chapter.objects.all()
    subchapters = SubChapter.objects.all()
    categories = Category.objects.all()

    context = {
        'years': years,
        'chapters': chapters,
        'subchapters': subchapters,
        'categories': categories,
    }

    return render(request, "file_upload.html", context)

# ✅ Display PDFs based on year, chapter, subchapter, and category
def show_data(request):
    year = request.GET.get('year')
    chapter1 = request.GET.get('chapter')
    subchapter = request.GET.get('subchapter')
    category = request.GET.get('category')

    print(f"Received year: {year}")  # Debugging
    print(f"Received chapter: {chapter1}")  
    print(f"Received subchapter: {subchapter}")  
    print(f"Received category: {category}")  
    
    # Ensure year exists
    year_obj = None
    chapters = []  # Default empty list
    if year:
        try:
            year_obj = get_object_or_404(Year, year=int(year))
            chapters = Chapter.objects.filter(year__year=int(year))
        except ValueError:
            year_obj = None  # Invalid input
    
    # Fetch PDFs only if category is provided
    PDFs = PDF.objects.filter(category__name=category) if category else PDF.objects.all()
    
    # Find chapter_subname
    chapter_subname = None  # ✅ Initialize before using
    for i in chapters:
        if i.name == chapter1:
            print(f"Found chapter: {i.name}")
            print(f"Subname: {i.subname}")
            chapter_subname = i.subname
            break
    else:
        print("No matching chapter found")

    print(f"Final chapter_subname: {chapter_subname}")  # Debugging

    context = {
        'year': year_obj,
        'chapter_name': chapter1,
        'chapter_subname': chapter_subname,
        'subchapter_name': subchapter,
        'category_name': category,
        'PDFs': PDFs,
    }

    return render(request, 'show_data.html', context)

# ✅ Logout View

@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

# ✅ Year List View (with nested relationships)
def year_list(request):
    years = Year.objects.prefetch_related('chapters__subchapters__categories__pdfs').all()
    return render(request, 'year_list.html', {'years': years})

# ✅ PDF Upload View (with form handling and debugging)
@login_required
def upload_pdf(request):
    selected_year = None
    selected_chapter = None
    selected_subchapter = None
    selected_category = None
    message = ""

    if request.method == "POST":
        year_id = request.POST.get('year')
        chapter_id = request.POST.get('chapter')
        subchapter_id = request.POST.get('subchapter')
        category_id = request.POST.get('category')
        pdf_file = request.FILES.get('file')

        if year_id and chapter_id and subchapter_id and category_id and pdf_file:
            category = get_object_or_404(Category, id=category_id)
            selected_year = get_object_or_404(Year, id=year_id)
            selected_chapter = get_object_or_404(Chapter, id=chapter_id)
            selected_subchapter = get_object_or_404(SubChapter, id=subchapter_id)

            # **Check for duplicates**
            if PDF.objects.filter(category=category, name=pdf_file.name).exists():
                message = "Error: A file with the same name already exists in this category."
            else:
                PDF.objects.create(category=category, name=pdf_file.name, file=pdf_file)
                message = "File uploaded successfully."

    # **Fetch today's uploaded PDFs**
    today = datetime.today().date()  # Get today's date
    pdfs_today = PDF.objects.filter(uploaded_at__date=today)  # Filter PDFs uploaded today

    return render(request, 'File_upload.html', {
        'message': message,
        'selected_year': selected_year,
        'selected_chapter': selected_chapter,
        'selected_subchapter': selected_subchapter,
        'selected_category': selected_category,
        'years': Year.objects.all(),
        'chapters': Chapter.objects.prefetch_related('subchapters__categories').all(),
        'categories': Category.objects.all(),
        'pdfs_today': pdfs_today  # Send today's PDFs to the template
    })

def get_subchapters(request):
    chapter_id = request.GET.get('chapter_id')
    subchapters = SubChapter.objects.filter(chapter_id=chapter_id).values('id', 'name')
    return JsonResponse(list(subchapters), safe=False)

def get_categories(request):
    subchapter_id = request.GET.get('subchapter_id')
    categories = Category.objects.filter(subchapter_id=subchapter_id).values('id', 'name')
    return JsonResponse(list(categories), safe=False)

def development(request):
    return render(request, 'dev_info.html')

def delete_pdf(request, pdf_id):
    pdf = get_object_or_404(PDF, id=pdf_id)

    if request.method == "POST":
        pdf.delete()

        # Get the referring URL (previous page)
        referer = request.META.get('HTTP_REFERER', reverse('show_data'))

        return HttpResponseRedirect(referer)  # Redirect to the previous page

    return redirect('show_data')         # Redirect to the PDF list page

def category_list(request):
    query = request.GET.get('q', '')  # Get the search query from the request
    if query:
        categories = Category.objects.filter(name__icontains=query)  # Case-insensitive search
    else:
        categories = Category.objects.all()
    
    return render(request, 'base.html', {'categories': categories, 'query': query})
