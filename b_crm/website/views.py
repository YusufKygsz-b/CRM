# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login, logout
# from .forms import SignUpForm, AddRecordForm
# from .models import Record
# from notifications.signals import notify
# from notifications.models import Notification
# from django.contrib.auth.models import User
# from django.http import JsonResponse

# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync


# def my_view(request):
#     # Bildirim oluşturma işlemi
#     user = request.user
#     notify.send(user, recipient=user, verb='Yeni bir bildirim!')

#     # Kanal katmanı
#     channel_layer = get_channel_layer()
#     async_to_sync(channel_layer.group_send)(
#         f"user_{user.id}",
#         {
#             'type': 'notification_message',
#             'verb': 'Yeni bir bildirim!'
#         }
#     )

# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync


# def home(request):
#     records = Record.objects.all()
#     notifications = []

#     if request.user.is_authenticated:
#         notifications = Notification.objects.filter(recipient=request.user, deleted=False).order_by('-timestamp')

#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             print(f"Authenticated user: {user}")
#             notify.send(user, recipient=user, verb='Giriş yaptınız!')
#             return redirect('home')
#         else:
#             if request.user.is_authenticated:
#                 notify.send(request.user, recipient=request.user, verb='Girişte bir hata oluştu, Lütfen Tekrar Deneyiniz...')
#             return redirect('home')

#     return render(request, 'home.html', {'records': records, 'notifications': notifications})


# def logout_user(request):
#     if request.user.is_authenticated:
#         user = request.user
#         logout(request)
#         notify.send(user, recipient=user, verb='Çıkış yaptınız...')
#         return redirect('home')
#     else:
#         return redirect('home')
    
# def register_user(request):
#     if request.method == "POST":
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password1']
#             user = authenticate(username=username, password=password)
#             login(request, user)
#             notify.send(user, recipient=user, verb='Başarılı bir şekilde kayıt oldunuz, Hoşgeldiniz')
#             return redirect('home')
#     else:
#         form = SignUpForm()
#     return render(request, 'register.html', {'form': form})

# def customer_record(request, pk):
#     if request.user.is_authenticated:
#         customer_record = Record.objects.get(id=pk)
#         return render(request, 'record.html', {'customer_record': customer_record})
#     else:
#         notify.send(None, recipient=request.user, verb='Bu Sayfayı Görüntülemek İçin Giriş Yapmış Olmalısınız...')
#         return redirect('home')

# def delete_record(request, pk):
#     if request.user.is_authenticated:
#         delete_it = Record.objects.get(id=pk)
#         delete_it.delete()
#         notify.send(request.user, recipient=request.user, verb='Kayıt Başarıyla Silindi...')
#         return redirect('home')
#     else:
#         notify.send(None, recipient=request.user, verb='Bunu Yapmak İçin Giriş Yapmış Olmalısınız...')
#         return redirect('home')

# def add_record(request):
#     form = AddRecordForm(request.POST or None)
#     if request.user.is_authenticated:
#         if request.method == "POST":
#             if form.is_valid():
#                 form.save()
#                 notify.send(request.user, recipient=request.user, verb='Kayıt Eklendi...')
#                 return redirect('home')
#         return render(request, 'add_record.html', {'form': form})
#     else:
#         notify.send(None, recipient=request.user, verb='Giriş Yapmış Olmalısınız...')
#         return redirect('home')

# def update_record(request, pk):
#     if request.user.is_authenticated:
#         current_record = Record.objects.get(id=pk)
#         form = AddRecordForm(request.POST or None, instance=current_record)
#         if form.is_valid():
#             form.save()
#             notify.send(request.user, recipient=request.user, verb='Record Has Been Updated!')
#             return redirect('home')
#         return render(request, 'update_record.html', {'form': form})
#     else:
#         notify.send(None, recipient=request.user, verb='You Must Be Logged In...')
#         return redirect('home')

# def mark_as_deleted(request, id):
#     if request.method == 'POST':
#         try:
#             notification = Notification.objects.get(id=id)
#             notification.deleted = True
#             notification.save()
#             return JsonResponse({'status': 'success'})
#         except Notification.DoesNotExist:
#             return JsonResponse({'status': 'error', 'message': 'Notification not found'}, status=404)
#     else:
#         return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, AddRecordForm
from .models import Record
from notifications.signals import notify
from notifications.models import Notification
from django.contrib.auth.models import User
from django.http import JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def send_notification_to_all_users(verb):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "notifications",  # Genel kanal adı
        {
            'type': 'send_notification',
            'verb': verb
        }
    )

def home(request):
    records = Record.objects.all()
    notifications = []

    if request.user.is_authenticated:
        notifications = Notification.objects.filter(recipient=request.user, deleted=False).order_by('-timestamp')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            notify.send(user, recipient=user, verb='Giriş yaptınız!')
            send_notification_to_all_users('Yeni giriş yapıldı!')
            return redirect('home')
        else:
            if request.user.is_authenticated:
                notify.send(request.user, recipient=request.user, verb='Girişte bir hata oluştu, Lütfen Tekrar Deneyiniz...')
            return redirect('home')

    return render(request, 'home.html', {'records': records, 'notifications': notifications})

def logout_user(request):
    if request.user.is_authenticated:
        user = request.user
        logout(request)
        notify.send(user, recipient=user, verb='Çıkış yaptınız...')
        send_notification_to_all_users('Bir kullanıcı çıkış yaptı!')
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
        send_notification_to_all_users('Bir kayıt silindi!')
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
                message = 'Kayıt Eklendi...'
                notify.send(request.user, recipient=request.user, verb=message)
                send_notification_to_all_users(message)  # Tüm kullanıcılara bildirim gönder
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
            message = 'Kayıt Güncellendi!'
            notify.send(request.user, recipient=request.user, verb=message)
            send_notification_to_all_users(message)  # Tüm kullanıcılara bildirim gönder
            return redirect('home')
        return render(request, 'update_record.html', {'form': form})
    else:
        notify.send(None, recipient=request.user, verb='Giriş Yapmış Olmalısınız...')
        return redirect('home')

def mark_as_deleted(request, id):
    if request.method == 'POST':
        try:
            notification = Notification.objects.get(id=id)
            notification.deleted = True
            notification.save()
            return JsonResponse({'status': 'success'})
        except Notification.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Notification not found'}, status=404)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
