# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login, logout
# from django.contrib import messages
# from .forms import SignUpForm, AddRecordForm
# from .models import Record
# from notifications.signals import notify

# # Create your views here.

# def home(request):

#     records = Record.objects.all()

#     # Check to see if loggin in
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']

#         # Authenticate
#         user = authenticate(request, username = username, password = password)
#         if user is not None:
#             login(request, user)
#             messages.success(request, "Giriş yaptınız!")
#             return redirect('home')
#         else:
#             messages.success(request, "Girişte bir hata oluştu, Lütfen Tekrar Deneyiniz...")
#             return redirect('home')
        
#     else:    
#         return render(request, 'home.html', {'records': records})

# def logout_user(request):
#     logout(request)
#     messages.success(request, "Çıkış yaptınız...")
#     return redirect('home')

# def register_user(request):
#     if request.method == "POST":
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password1']
#             user = authenticate(username = username, password =  password)
#             login(request, user)
#             messages.success(request, "Başarılı bir şekilde kayıt oldunuz, Hoşgeldiniz")
#             return redirect('home')
    
#     else:
#         form = SignUpForm()
#         return render(request, 'register.html', {'form':form})

#     return render(request, 'register.html', {'form':form})

# def customer_record(request, pk):
# 	if request.user.is_authenticated:
# 		# Look Up Records
# 		customer_record = Record.objects.get(id=pk)
# 		return render(request, 'record.html', {'customer_record':customer_record})
# 	else:
# 		messages.success(request, "Bu Sayfayı Görüntülemek İçin Giriş Yapmış Olmalısınız...")
# 		return redirect('home')

# def delete_record(request, pk):
# 	if request.user.is_authenticated:
# 		delete_it = Record.objects.get(id=pk)
# 		delete_it.delete()
# 		messages.success(request, "Kayıt Başarıyla Silindi...")
# 		return redirect('home')
# 	else:
# 		messages.success(request, "Bunu Yapmak İçin Giriş Yapmış Olmalısınız...")
# 		return redirect('home')
      
# def add_record(request):
# 	form = AddRecordForm(request.POST or None)
# 	if request.user.is_authenticated:
# 		if request.method == "POST":
# 			if form.is_valid():
# 				add_record = form.save()
# 				messages.success(request, "Kayıt Eklendi...")
# 				return redirect('home')
# 		return render(request, 'add_record.html', {'form':form})
# 	else:
# 		messages.success(request, "Giriş Yapmış Olmalısınız...")
# 		return redirect('home')
	
# def update_record(request, pk):
# 	if request.user.is_authenticated:
# 		current_record = Record.objects.get(id=pk)
# 		form = AddRecordForm(request.POST or None, instance=current_record)
# 		if form.is_valid():
# 			form.save()
# 			messages.success(request, "Record Has Been Updated!")
# 			return redirect('home')
# 		return render(request, 'update_record.html', {'form':form})
# 	else:
# 		messages.success(request, "You Must Be Logged In...")
# 		return redirect('home')




from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, AddRecordForm
from .models import Record
from notifications.signals import notify
from notifications.models import Notification
from django.contrib.auth.models import User
from honeypot.decorators import check_honeypot


# @check_honeypot(field_name='username')
def home(request):
    records = Record.objects.all()
    notifications = []

    if request.user.is_authenticated:
        notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            notify.send(user, recipient=user, verb='Giriş yaptınız!')
            return redirect('home')
        else:
            notify.send(user, recipient=user, verb='Girişte bir hata oluştu, Lütfen Tekrar Deneyiniz...')
            return redirect('home')

    return render(request, 'home.html', {'records': records, 'notifications': notifications})

def logout_user(request):
    if request.user.is_authenticated:
        user = request.user
        logout(request)
        notify.send(user, recipient=user, verb='Çıkış yaptınız...')
        return redirect('home')
    else:
        return redirect('home')
    
def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            notify.send(user, recipient=user, verb='Başarılı bir şekilde kayıt oldunuz, Hoşgeldiniz')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})

def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record': customer_record})
    else:
        notify.send(None, recipient=request.user, verb='Bu Sayfayı Görüntülemek İçin Giriş Yapmış Olmalısınız...')
        return redirect('home')

def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        notify.send(request.user, recipient=request.user, verb='Kayıt Başarıyla Silindi...')
        return redirect('home')
    else:
        notify.send(None, recipient=request.user, verb='Bunu Yapmak İçin Giriş Yapmış Olmalısınız...')
        return redirect('home')

def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                form.save()
                notify.send(request.user, recipient=request.user, verb='Kayıt Eklendi...')
                return redirect('home')
        return render(request, 'add_record.html', {'form': form})
    else:
        notify.send(None, recipient=request.user, verb='Giriş Yapmış Olmalısınız...')
        return redirect('home')

def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            notify.send(request.user, recipient=request.user, verb='Record Has Been Updated!')
            return redirect('home')
        return render(request, 'update_record.html', {'form': form})
    else:
        notify.send(None, recipient=request.user, verb='You Must Be Logged In...')
        return redirect('home')
