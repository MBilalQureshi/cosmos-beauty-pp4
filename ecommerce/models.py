from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.core.validators import MinValueValidator, MaxValueValidator
from autoslug import AutoSlugField


class ShipmentDetail(models.Model):
    """
    User Payment Modal
    """
    PAYMENT_METHOD_CHOICES = [
        (0, "COD(Cash on delivery)"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="user_address")
    first_name = models.CharField(max_length=30, null=False, blank=False)
    last_name = models.CharField(max_length=30, null=False, blank=False)
    address_line_one = models.CharField(max_length=120, null=False,
                                        blank=False)
    postal_code = models.PositiveIntegerField(null=False, blank=False,
                                              validators=[
                                                  MaxValueValidator(999999)
                                                  ])
    city = models.CharField(max_length=40, null=False, blank=False)
    country = models.CharField(max_length=40, null=False, blank=False)
    mobile = models.BigIntegerField(unique=True, null=False, blank=False,
                                    validators=[
                                      MaxValueValidator(9999999999999)
                                      ])
    method = models.IntegerField(choices=PAYMENT_METHOD_CHOICES, default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class ProductCategories(models.Model):
    """
    Product Categories Modal
    """
    category_name = models.CharField(max_length=150, blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category_name


class ProductDiscount(models.Model):
    """
    Product Discount Modal
    """
    discount_name = models.CharField(max_length=150, blank=False)
    discount_percentage = models.PositiveIntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(100)
    ])
    active = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.discount_name


class Product(models.Model):
    """
    Product Modal
    """
    sku = models.CharField(max_length=16, blank=True)
    name = models.CharField(max_length=200, blank=False)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=False)
    image = CloudinaryField('image', default='placeholder')
    available = models.BooleanField(default=False)
    stock = models.PositiveIntegerField(default=0, null=False)
    product_category = models.ForeignKey(ProductCategories,
                                         on_delete=models.CASCADE,
                                         related_name="product_category")
    discount_name = models.ForeignKey(ProductDiscount, default=1,
                                      on_delete=models.SET_DEFAULT,
                                      related_name="product_discount")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    slug = AutoSlugField(populate_from='name', unique=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.name


class UserBill(models.Model):
    """
    User Bill Modal
    """
    user_info = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name="user_bill_info")
    shipment_info = models.ForeignKey(ShipmentDetail, on_delete=models.CASCADE,
                                      related_name="user_shipment_info")
    total = models.DecimalField(max_digits=6, decimal_places=2)
    user_unique_order_no = models.CharField(max_length=10, editable=False,
                                            unique=True,)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_on']


class ConfirmedOrderDetail(models.Model):
    """
    Confirmed Order Modal
    """
    SHIPMENT_STAUS = [
        (0, 'Order Received'),
        (1, 'Order On way'),
        (3, 'Order Delieverd')
    ]
    user_info = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name="user_confirmed_order")
    product_info = models.ForeignKey(Product, on_delete=models.CASCADE,
                                     related_name="user_bought_product")
    quantity = models.PositiveIntegerField(null=False, blank=False, default=1,
                                           validators=[
                                            MinValueValidator(1),
                                            MaxValueValidator(10)])
    prod_total = models.DecimalField(max_digits=6, decimal_places=2)
    user_unique_order_no = models.CharField(max_length=10, editable=False,)
    order_status = models.IntegerField(choices=SHIPMENT_STAUS, default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f"{self.user_info.first_name} {self.user_info.last_name}"


class Wishes(models.Model):
    """
    Wishlist Modal
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="userid")
    wish = models.ForeignKey(Product, on_delete=models.CASCADE,
                             related_name="user_wish")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']
        verbose_name_plural = 'Wishes'
