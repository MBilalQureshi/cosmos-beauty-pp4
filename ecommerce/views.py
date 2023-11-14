from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.views import generic, View
from .models import ShipmentDetail, ProductCategories, ProductDiscount, Product, CartItem, ConfirmedOrderDetail, Wishes, UserBill
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import datetime
from django.conf import settings
import decimal
from django.db.models import Q
from .forms import ShipmentDetailForm
import random


class Home (generic.TemplateView):
    """
    """
    template_name = 'index.html'


class Products (generic.ListView):
    """
    Fetch products data from database and display on
    products.html
    """
    # TASK: CHECK IF DICOUNT EXIST OR NOT
    queryset = Product.objects.filter(available=True).filter(stock__gt=0).order_by('-created_on')
    template_name = 'products.html'
    paginate_by = 12


class ProductsCategory (generic.ListView):
    """
    Fetch products data from database and display on
    products.html
    """
    # TASK: CHECK IF DICOUNT EXIST OR NOT
    queryset = Product.objects.filter(available=True).filter(stock__gt=0).order_by('-created_on')
    template_name = 'products.html'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        category_param = self.kwargs.get("category")
        category = ProductCategories.objects.get(category_name=category_param)
        products =  Product.objects.filter(product_category=category).filter(available=True).filter(stock__gt=0).order_by('-created_on')
        return {'product_list': products}


class SpecialOffers (generic.ListView):
    queryset = Product.objects.filter(available=True).filter(stock__gt=0).filter(~Q(discount_name = 2)).order_by('-created_on')
    template_name = 'products.html'
    paginate_by = 12


class ProductDetail(generic.DetailView):
    def get(self, request, slug, *args, **kwargs):
        queryset = Product.objects.filter(stock__gt=0).filter(slug=slug).order_by('-created_on')
        product = get_object_or_404(queryset)
        # check if product is added to wishlist
        # wish_id=product.id ??????????????

        discount = 0
        if product.discount_name.discount_percentage > 0:
            discount = (float(product.discount_name.discount_percentage) * float(product.price)) / 100
            discount = product.price-decimal.Decimal(discount)

        product_wish = False
        add_to_cart = False
        if request.user.is_authenticated:
            if(Wishes.objects.filter(user=request.user, wish_id=product.id)):
                product_wish = True
            else:
                product_wish = False
        if request.session.get('cart') is not None:
            if str(product.id) in request.session.get('cart'):
                add_to_cart = True
            else:
                add_to_cart = False
        return render(
            request,
            "product_detail.html",
            {
                'product': product,
                'product_wish': product_wish,
                'add_to_cart':add_to_cart,
                'discount':discount,
            },
        )


@login_required(login_url='/accounts/login/')
def wishlist(request):
    wishlist = Wishes.objects.filter(user=request.user)
    context = {'wishlist':wishlist}
    return render(request, 'wishlist.html',context)

# only adding and removing from wishlist
class AddToWishlist(View):
    def post(self, request):
        if request.method == 'POST':
            if request.user.is_authenticated:
                prod_id = int(request.POST.get('productId'))
                product_check = Product.objects.get(id=prod_id)
                if(product_check):
                    if(Wishes.objects.filter(user=request.user, wish_id=prod_id)):
                        # return JsonResponse('status', 'Product already in wishlist')
                        # remove from wishlist
                        wish_delete = get_object_or_404(Wishes, user=request.user, wish_id=prod_id)
                        wish_delete.delete()
                    else:
                        # add to wish list
                        Wishes.objects.create(user=request.user, wish_id=prod_id)
                else:
                    return JsonResponse('status', 'Login to continue')
        else:
            return JsonResponse({'status', "Login to continue"})
        return redirect('/')


# @login_required(login_url='/accounts/login/')
def cart(request):
    if request.method == 'POST':
        # When in cart remove item from cart
        cart = request.session.get(settings.CART_SESSION_ID)
        request.session.cart = cart
        prod_id = str(request.POST.get('productId'))
        del request.session.cart[prod_id]
        request.session.modified = True
        return redirect('/')
    total = 0.00
    ship_total = 5.00
    if request.session.get('cart') is not None and request.session.get('cart'):
        # cart = request.session.get('cart')
        ids = []
        
        for key,value in request.session.get('cart').items():
            # print("135", request.session.get('cart').items())
            total += value['prod_total']
            print(f'Key: {key}, Value: {value}')

            ids += key
        products = Product.objects.filter(available=True).filter(stock__gt=0).filter(id__in=ids)
        # for i in range(len(products)):
        #     # products[i].append({'quantity':1})
        #     products[i]["quantity"] = 3
        # print(products)
        # for p in products:
        #     print(p)
        print(total)
        ship_total = round(ship_total + total,2)
    else:
        # TASK HANDLE EMPTY CART
        products = []
        cart = 'Nothing in cart'
    context = {'products':products, 'total':total, 'ship_total': ship_total,}
    return render(request, 'cart.html', context)



class AddToCart(View):
    def post(self, request):
        if request.method == 'POST':
            prod_id = str(request.POST.get('productId'))
            prod_quantity = int(request.POST.get('productQuantity'))
            product_price = float(request.POST.get('price'))
            if request.POST.get('discount') is not None:
                prod_discount = float(request.POST.get('discount'))
                prod_total = prod_discount * prod_quantity
            else:
                prod_discount = 0.0
                prod_total = product_price * prod_quantity
            self.session = request.session
            cart = self.session.get(settings.CART_SESSION_ID)
            # empty cart saved in session
            if not cart:
                cart = self.session[settings.CART_SESSION_ID]={}
            self.cart = cart
            # prod_id = int(prod_id)
            if prod_id not in self.cart:
                self.cart[prod_id]={'quantity':prod_quantity, 'price':product_price, 'discount':prod_discount, 'prod_total':prod_total}
            else:
                del self.cart[prod_id]
            request.session.modified = True
            print(self.cart)
            return redirect('/')
    #         request.session.clear()
    # request.session.flush()
        else:
            return redirect('/')


class Checkout(View):
    def get(self, request):
        if request.user.is_authenticated:
            # get user data if avalable
            get_user_last_data = ShipmentDetail.objects.filter(user=request.user)
            if get_user_last_data:
                instance = get_object_or_404(get_user_last_data, user=request.user)
                print(instance.first_name)
                form = ShipmentDetailForm(instance = instance)
            else:
                # set to empty form if data not available
                form = ShipmentDetailForm()
        return render(
            request,
            "user_checkout.html",
            {
                'form': form,
            },
        )

    def post(self, request):
        if request.user.is_authenticated:
            get_user_last_data = ShipmentDetail.objects.filter(user=request.user)
            if get_user_last_data:
                # update form
                instance = get_object_or_404(ShipmentDetail, user=request.user)
                form = ShipmentDetailForm(request.POST,instance = instance)
                if form.is_valid():
                    fetch_user = form.save(commit=False)
                    fetch_user.user = request.user
                    form.save()
            else:
                # First time add form
                form = ShipmentDetailForm(request.POST)
                if form.is_valid():
                    fetch_user = form.save(commit=False)
                    fetch_user.user = request.user
                    form.save()


    
                    
            # form = ShipmentDetailForm()
            # check if current user address, name, email exist show them in box and ask if need to edit also shipping method
            # cart = request.session.get(settings.CART_SESSION_ID)
            # request.session.cart = cart

            overall_total = 0.00
            invoice_no = create_new_ref_number()
            print(invoice_no)
            # TASK UPDATE THE QUANTITY IN PRODUCTS STOCK
            for key,value in request.session.get('cart').items():
            # print("135", request.session.get('cart').items())
                # print(f'Key: {key}, Value: {value}')
                overall_total += value['prod_total']
                prod_id = Product.objects.get(id=key)
                add_confirmed_order = ConfirmedOrderDetail(user_info=request.user, product_info=prod_id, quantity=value['quantity'],prod_total = value['prod_total'],user_unique_order_no=invoice_no)
                add_confirmed_order.save()
            
            overall_total = round(5.00 + overall_total,2)
            user_shipment_id = ShipmentDetail.objects.get(user=request.user)
            user_bill_ref = UserBill(user_info=request.user,shipment_info= user_shipment_id ,total=overall_total,user_unique_order_no=invoice_no)
            user_bill_ref.save()
            del request.session['cart']
        return render(
            request,
            "order_complete.html",
            {
                'form': form,
            },
        )

    def create_new_ref_number():
        not_unique = True
        while not_unique:
            unique_ref = random.randint(1000000000, 9999999999)
            if not ConfirmedOrderDetail.objects.filter(user_unique_order_no=unique_ref):
                not_unique = False
        return str(unique_ref)

class MyOrders(View):

    def get(self, request):
        get_products ={}
        if request.user.is_authenticated:
            # get user invoices
            get_invoice_list = UserBill.objects.filter(user_info=request.user).values_list('user_unique_order_no',flat = True)
            if get_invoice_list:          
                index = 0
                for invoice_number in get_invoice_list:
                    # print(invoice_number)
                    # get products data based on invoice numbers
                    get_products[index] = ConfirmedOrderDetail.objects.filter(user_unique_order_no = invoice_number).values_list('product_info','product_info__image','product_info__name','quantity','prod_total', 'product_info__stock')
                    # print(get_products)
                    # print(index)
                    index += 1
                # print(get_products)
                # for key, value in get_products.items():
                #     print(f"Key: {key} Value:{value}")
                
                # print(value)
                # for product in value:
                #     # product_name, quantity, price = product
                #     print(f"  Product: {product_name}, Quantity: {quantity}, Price: {price}")
                # for product in get_products:
                #     product_name, quantity, price = product
                    # print(f"Product: {product_name}, Quantity: {quantity}, Price: {price}")
            # Logic to seperate oders
            else:
                # TASK handle below on front later
                print("No invoices available")            
            
        return render(
            request,
            "my_orders.html",
            {
                'get_products':get_products,
            },
        )
    def post(self,request):
        return render(
            request,
            "my_orders.html",
            {
                
            },
        )
    # queryset = Product.objects.filter(available=True).filter(stock__gt=0).order_by('-created_on')
    # template_name = 'my_orders.html'
    # paginate_by = 12
