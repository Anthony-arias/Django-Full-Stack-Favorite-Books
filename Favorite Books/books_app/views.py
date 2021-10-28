from django.shortcuts import render, redirect
from .models import User, Book
from django .contrib import messages
import bcrypt


def view_login_register(request):
    if 'userid' in request.session:
        print('User is already in session')
        request.session.clear()
    else:
        print("user not in session")
    print("in view login registration")
    return render(request, "login-register.html")

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    print("in registration form")
    password = request.POST['user_password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    User.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'],email=request.POST['user_email'],hashed_pw=pw_hash)
    request.session['userid'] = User.objects.last().id
    return redirect("/books")

def login(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    user = User.objects.filter(email=request.POST['user_email'])
    if user:
        print("user in database")
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['user_password'].encode(), logged_user.hashed_pw.encode()):
            print("checked pw")
            request.session['userid'] = logged_user.id
            print("email " + request.POST['user_email'])
            print("password " + request.POST['user_password'])
            print("user id " + str(logged_user.id))
            return redirect("/books")
    print('user not in database')
    return redirect("/")

def showBooks(request):
    try:
        context = {
        "user": User.objects.get(id=request.session['userid']),
        "books": Book.objects.all()
        }
    except:
        return redirect('/')
    
    return render(request, "books.html", context)

def logOut(request):
    request.session.clear()
    return redirect('/')

def decideWhatToShow(request, book_id):
    if 'userid' not in request.session:
        return redirect('/')

    this_book = Book.objects.get(id=book_id)
    this_user = User.objects.get(id=request.session['userid'])
    context = {
        "book": this_book,
        "user": this_user
        }
    
    if this_book.upload_by == this_user:
        return render(request, "edit-book.html", context)
    else:
        return render(request, "show-book.html", context)

def addBook(request):
    if 'userid' not in request.session:
        return redirect('/')

    errors = Book.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/books")
    this_user = User.objects.get(id=request.session['userid'])
    Book.objects.create(title=request.POST['book_title'],desc=request.POST['book_desc'],upload_by=this_user)
    this_book = Book.objects.last()
    this_user.like_books.add(this_book)
    return redirect("/books")

def removeFavorite(request, book_id):
    if 'userid' not in request.session:
        return redirect('/')

    this_book = Book.objects.get(id=book_id)
    this_user = User.objects.get(id=request.session['userid'])
    this_user.like_books.remove(this_book)
    return redirect("/book/"+str(book_id))

def addFavorite(request, book_id):
    if 'userid' not in request.session:
        return redirect('/')

    this_book = Book.objects.get(id=book_id)
    this_user = User.objects.get(id=request.session['userid'])
    this_user.like_books.add(this_book)
    return redirect("/books")

def editBook(request, book_id):
    if 'userid' not in request.session:
        return redirect('/')

    this_book = Book.objects.get(id=book_id)
    if request.POST['button'] == "add":
        this_book.title = request.POST['book_title']
        this_book.desc = request.POST['book_desc']
        this_book.save()
    else:
        this_book.delete()
    
    return redirect("/books")