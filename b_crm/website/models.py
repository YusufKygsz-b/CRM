from django.db import models
from django.utils import timezone
from PIL import Image

class Record(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=20)
    is_deleted = models.BooleanField(default=False)  # Yeni alan

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        verbose_name = 'Kayıt'
        verbose_name_plural = 'Kayıtlar'


class Supplier(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    address = models.TextField()
    contact_number = models.CharField(max_length=20)
    contact_person_first_name = models.CharField(max_length=100)
    contact_person_last_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name

# Ürün modelini temsil eden model
class Product(models.Model):
    # existing fields
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    arrival_date = models.DateField()
    processing_start_date = models.DateField(blank=True, null=True)
    processing_end_date = models.DateField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    image = models.ImageField(null=True, blank=True, upload_to='product_images/%Y/%m/')

    @property
    def waiting_period(self):
        if self.is_completed:
            return (self.processing_end_date - self.arrival_date).days
        else:
            today = timezone.now().date()
            return (today - self.arrival_date).days

    def save(self, *args, **kwargs):
        if self.processing_end_date and self.processing_end_date <= timezone.now().date():
            self.is_completed = True
        else:
            self.is_completed = False
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 600 or img.width > 600:
                output_size = (600, 600)
                img.thumbnail(output_size)
                img.save(self.image.path)

    def __str__(self):
        return self.name
    

# Stok modelini temsil eden model
class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stocks')
    entry_date = models.DateField()
    exit_date = models.DateField(blank=True, null=True)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.product.name} - {self.quantity}'

    class Meta:
        ordering = ['-entry_date']