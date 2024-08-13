from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name= 'register'),
    path('record/<int:pk>', views.customer_record, name='record'),
    path('delete_record/<int:pk>', views.delete_record, name='delete_record'),
    path('add_record/', views.add_record, name='add_record'),
    path('update_record/<int:pk>', views.update_record, name='update_record'),

    # Supplier URLs
    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('suppliers/<int:pk>/', views.supplier_detail, name='supplier_detail'),
    path('suppliers/add/', views.add_supplier, name='add_supplier'),
    path('suppliers/<int:pk>/edit/', views.update_supplier, name='update_supplier'),
    path('suppliers/<int:pk>/delete/', views.delete_supplier, name='delete_supplier'),  # URL deseni

    # Product URLs
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/<int:pk>/edit/', views.update_product, name='update_product'),
    path('products/<int:pk>/delete/', views.delete_product, name='delete_product'),

    # Stock URLs
    path('stocks/', views.stock_list, name='stock_list'),
    path('stocks/<int:pk>/', views.stock_detail, name='stock_detail'),
    path('stocks/add/', views.add_stock, name='add_stock'),
    path('stocks/<int:pk>/edit/', views.update_stock, name='update_stock'),
    path('stocks/<int:pk>/delete/', views.delete_stock, name='delete_stock'),

    path('api/notifications/<int:id>/mark-as-deleted/', views.mark_as_deleted, name='mark_as_deleted'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
