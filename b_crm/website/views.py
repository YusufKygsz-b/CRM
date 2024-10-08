
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
from django.db.models import Q
import unicodedata
from django.utils.translation import gettext as _
from django.utils.translation import get_language, activate, gettext

from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from .models import Supplier
from .serializers import SupplierSerializer
from django_filters.rest_framework import DjangoFilterBackend

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
            # Get updated count
            notification_count = Notification.objects.filter(recipient=request.user, deleted=False).count()
            return JsonResponse({'status': 'success', 'notification_count': notification_count})
        except Notification.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Notification not found'}, status=404)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


## Supplier Managment Views Code ## 
from django.shortcuts import render, get_object_or_404, redirect
from .models import Supplier, Product, Stock
from .forms import SupplierForm, ProductForm, StockForm

def normalize_text(text):
    # Unicode karakterleri normalize eder
    text = unicodedata.normalize('NFKD', text)
    return text.lower()

def adjust_query_for_i(query):
    # Küçük "i" ve büyük "İ" ile arama yapacak şekilde sorguyu ayarla
    query_with_i = query
    query_with_I = query.replace('i', 'İ')
    return Q(name__icontains=query_with_i) | Q(city__icontains=query_with_i) | \
           Q(name__icontains=query_with_I) | Q(city__icontains=query_with_I)
# Supplier Views

def translate(language):
    cur_language = get_language()
    try:
        activate(language)
        text = gettext('hello')
    finally:
        activate(cur_language)
    return text

def supplier_list(request):
    query = request.GET.get('q', '').strip()
    trans = None  # Varsayılan değer atayın
    if query:
        suppliers = Supplier.objects.filter(Q(name__icontains=query) | Q(city__icontains=query))
        if not suppliers.exists():
            normalized_query = normalize_text(query)
            search_filter = adjust_query_for_i(normalized_query)
            suppliers = Supplier.objects.filter(search_filter)
    else:
        suppliers = Supplier.objects.all()
        trans = translate(language='fr')  # `trans` değerini burada alabilirsiniz
        
    return render(request, 'Supplier/supplier_list.html',
                  {'suppliers': suppliers, 'trans': trans})

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('name', 'city')  # Arama yapabileceğiniz alanlar


def supplier_detail(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    trans = translate(language='en')  # Varsayılan dil ayarı, burada 'fr' (Fransızca) kullanılıyor.
    return render(request, 'Supplier/supplier_detail.html', {'supplier': supplier, 'trans': trans})


def add_supplier(request):
    if request.method == "POST":
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
    else:
        form = SupplierForm()
    return render(request, 'Supplier/add_supplier.html', {'form': form})

def update_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == "POST":
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'Supplier/update_supplier.html', {'form': form})

def delete_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    supplier.delete()
    return redirect('supplier_list')



## Product Views ##
from django.shortcuts import render
from django.db.models import Sum

def product_list(request):
    products = Product.objects.all()

    # Calculate earnings
    completed_products = products.filter(is_completed=True)
    ongoing_products = products.filter(is_completed=False)

    completed_earnings = completed_products.aggregate(total=Sum('sale_price'))['total'] or 0
    ongoing_earnings = ongoing_products.aggregate(total=Sum('sale_price'))['total'] or 0
    total_earnings = products.aggregate(total=Sum('sale_price'))['total'] or 0

    context = {
        'products': products,
        'completed_earnings': completed_earnings,
        'ongoing_earnings': ongoing_earnings,
        'total_earnings': total_earnings,
    }
    return render(request, 'Product/product_list.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'Product/product_detail.html', {'product': product})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')  # Redirect to the product list after saving
    else:
        form = ProductForm()
    
    suppliers = Supplier.objects.all()
    return render(request, 'Product/add_product.html', {'form': form, 'suppliers': suppliers})

def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    suppliers = Supplier.objects.all()  # Fetch all suppliers
    return render(request, 'Product/update_product.html', {'form': form, 'suppliers': suppliers, 'product': product})
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('product_list')


## Stock Views
def stock_list(request):
    stocks = Stock.objects.all()
    return render(request, 'Stock/stock_list.html', {'stocks': stocks})

def stock_detail(request, pk):
    stock = get_object_or_404(Stock, pk=pk)
    return render(request, 'Stock/stock_detail.html', {'stock': stock})

def add_stock(request):
    products = Product.objects.all()  # Ürünleri al
    if request.method == "POST":
        form = StockForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('stock_list')
    else:
        form = StockForm()
    return render(request, 'Stock/add_stock.html', {'form': form, 'products': products})

def update_stock(request, pk):
    stock = get_object_or_404(Stock, pk=pk)
    products = Product.objects.all()  # Ürünleri al
    if request.method == "POST":
        form = StockForm(request.POST, instance=stock)
        if form.is_valid():
            form.save()
            return redirect('stock_list')
    else:
        form = StockForm(instance=stock)
    return render(request, 'Stock/update_stock.html', {'form': form, 'products': products})

def delete_stock(request, pk):
    stock = get_object_or_404(Stock, pk=pk)
    stock.delete()
    return redirect('stock_list')