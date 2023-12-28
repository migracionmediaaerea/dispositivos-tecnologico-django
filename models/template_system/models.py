from random import randrange

from django.contrib.auth.models import AbstractUser
from django.db import models
from safedelete.models import SOFT_DELETE_CASCADE, SafeDeleteModel
from simple_history.models import HistoricalRecords

from apps.comun.models import AbstractModel, AbstractNullableModel


class User(AbstractUser, AbstractNullableModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    image = models.ImageField(upload_to='profiles/', max_length=255, blank=True, null=True, default='profiles/generic/blank-profile-pic.png')
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)
    dark_mode = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['id']

class Movie(AbstractModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    title = models.CharField(max_length=100)
    year = models.IntegerField()
    genre = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    plot = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'Movie' 
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'

class Sale(AbstractModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    encargado = models.ForeignKey('User', on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Sale' 
        verbose_name = 'Sale'
        verbose_name_plural = 'Sales'

class MovieSales(AbstractModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'MovieSale' 
        verbose_name = 'MovieSale'
        verbose_name_plural = 'MovieSales'

def random_image_chooser():
    """This defines the default image for the user"""


    from django.db import models



# Model for Django Rest Framework example
class Animals(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    
    DIET_CHOICES = (
        ('MT', 'Meat'),
        ('PL', 'Plant'),
        ('OM', 'Omnivores'),
    )
    
    
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    diet = models.CharField(max_length=3, choices=DIET_CHOICES, )
    
    class Meta:
        db_table = 'animals'
        verbose_name = 'Animal'
        verbose_name_plural = 'Animals'