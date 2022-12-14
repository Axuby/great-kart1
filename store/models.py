
from django.db.models import Q
from django.urls import reverse
from django.db import models
from category.models import Category
# Create your models here.


class ProductQueryset(models.QuerySet):
    def is_public(self):
        return self.filter(is_available=True)

    def search(self, query, user=None):
        lookup = Q(product_name__icontains=query) | Q(
            description__icontains=query)
        qs = self.is_public().filter(lookup)
        if user is not None:
            qs2 = self.filter(user=user)
            qs = (qs | qs2).distinct()
        return qs


class ProductManager(models.Manager):

    def get_queryset(self, *args, **kwargs):

        return ProductQueryset(self.model, using=self._db)

    def search(self, query, user=None):
        return self.get_queryset().search(user=user)


class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=255)
    description = models.CharField(max_length=500, blank=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products")
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.product_name

    def get_absolute_url(self):
        return reverse("product-detail", args=[self.category.slug, self.slug])


class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).get_queryset().filter(variation_category='color', is_active=True)

    def size(self):
        return super(VariationManager, self).get_queryset().filter(variation_category='size', is_active=True)


class Variation(models.Model):
    variation_category_choices = (
        ('color', 'color'),
        ('size', 'size')
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(
        max_length=50, choices=variation_category_choices)
    variation_value = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self) -> str:
        return self.variation_value
