from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Store, Category, Product, Order, OrderItem
# Imports
import random
import string
from uuid import uuid4
from django.utils import timezone

def dashboard(request):
    return render(request, 'core/dashboard.html')

def storelist(request):
    store = Store.objects.all()
    print(store)
    context = {
        'stores' : store,
    }
    return render(request, 'core/storelist.html', context)

def add_store(request):
    if request.method == 'POST' and request.FILES:
        store_name = request.POST.get('store-name')
        store_address = request.POST.get('store-address')
        store_manager = request.POST.get('store-manager')
        store_image = request.FILES.get('store-image')
        store_slug = request.POST.get('store-slug')
        store_created = request.POST.get('store-created')


        print(store_name, store_address, store_manager, store_image)
        store_obj = Store.objects.create(
            store_name=store_name,
            store_address=store_address,
            store_manager=store_manager,
            store_image=store_image,
            store_slug=store_slug,
            store_created=store_created
        )
        store_obj.save()
        messages.success(request, 'Store added successfully')
        return redirect('storelist')

    return render(request, 'core/addstore.html')

def pos_dashboard(request, store_slug):
    store = get_object_or_404(Store, store_slug=store_slug)
    context = {
        'store' : store,
    }
    return render(request, 'core/pos_dashboard.html', context)

def categories(request, store_slug):
    store = get_object_or_404(Store, store_slug=store_slug)
    categories = Category.objects.filter(category_store=store)
    context = {
        'store' : store,
        'categories': categories
    }
    return render(request, 'core/categories.html', context)

def add_category(request, store_slug):
    str1 = ''.join((random.choice(string.ascii_letters) for x in range(3)))  
    str1 += ''.join((random.choice(string.digits) for x in range(3)))  
    print(str1)
    store = get_object_or_404(Store, store_slug=store_slug)
    if request.method == 'POST':
        category_name = request.POST.get('category-name')
        category_description = request.POST.get('category-description')
        category_slug = request.POST.get('category-slug')
        category_code = request.POST.get('category-code')
        category_store = request.POST.get('category-store')
        category_created = request.POST.get('category-date')
        
        print(category_name, category_description, category_slug, category_code, category_store, category_created)

        category_obj = Category.objects.create(
            category_name=category_name,
            category_slug=category_slug,
            category_code=category_code,
            category_description=category_description,
            category_store=store,
            category_created=category_created
        )
        category_obj.save()
        messages.success(request, "Successfully created category")
        return redirect('add_category', store_slug=store.store_slug)
    context = {
        'store' : store,
        'code' : str1
    }
    return render(request, 'core/addcategory.html', context)

def edit_category(request, store_slug, category_slug):
    store = get_object_or_404(Store, store_slug=store_slug)
    category = get_object_or_404(Category, category_slug=category_slug)

    context = {
        'store' : store,
        'category' : category
    }
    return render(request, 'core/editcategory.html', context)

def delete_category(request, store_slug, category_slug):
    store = get_object_or_404(Store, store_slug=store_slug)
    category = get_object_or_404(Category, category_slug=category_slug)
    category.delete()
    messages.success(request, 'Category deleted successfully')

    return redirect('categories', store_slug=store.store_slug)

def pointofsales(request, store_slug):
    store = get_object_or_404(Store, store_slug=store_slug)
    products = Product.objects.filter(product_store=store)
    categories = Category.objects.filter(category_store=store)
    order = Order.objects.filter(order_store=store)
    order_items = OrderItem.objects.filter(order_item_product__product_store=store)

    order_item = OrderItem.objects.filter(order_item_product__product_store=store, order_item_order__order_completed=False)
    order_completed = False

    for ord in order:
        order_completed = ord.order_completed
    print(order_completed)


    
    
    


    sort = request.GET.get('sort', None)
    category = request.GET.get('filter', None)

    order = []
    if sort == 'new':
        order.append('-product_created')
    elif sort == 'old':
        order.append('product_created')
    elif sort == 'price_desc':
        order.append('-product_price')
    elif sort == 'price_asc':
        order.append('product_price')
    
    if category and category != 'all':
        category = category.replace('-', ' ')
        products = products.filter(product_category__category_name=category)

    if order:
        products = products.order_by(*order)

    category = Category.objects.order_by('category_name').values('category_name').distinct()
    context = {
        'store' : store,
        'products' : products,
        'category' : category,
        'order_items': order_item,
        'order_completed': order_completed,
    }
    return render(request, 'core/pointofsales.html', context)

def order_item(request, store_slug, product_slug):
    store = get_object_or_404(Store, store_slug=store_slug)
    products = get_object_or_404(Product,product_slug=product_slug)
    product = Product.objects.filter(product_slug=product_slug)

    uuid = uuid4()
    truncate_uuid = str(uuid)[:6]
    print(truncate_uuid)


    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        total = request.POST.get('total')
        print(quantity, total)
        if(quantity == ''):
            messages.error(request, 'Please enter a quantity')
            return redirect('pos', store_slug=store_slug)
        else:
            order_obj = None


            if Order.objects.filter(order_completed=False).exists():
                order_obj = Order.objects.get(order_completed=False)
                # print(order_obj.id)
                print('Order Exists')



                for prd,qty in zip(product, quantity):
                    order_item_obj = OrderItem.objects.create(
                        order_item_id=truncate_uuid,
                        order_item_order=order_obj,
                        order_item_product=prd,
                        order_item_quantity=qty,
                        order_item_price=prd.product_price,
                        order_item_total=float(total),
                        order_item_created=timezone.now()
                    )
                    order_item_obj.save()

            else:
                print('Order Created')
                order_obj = Order.objects.create(
                    order_id=truncate_uuid,
                    order_store=store,
                    order_completed=False,
                    order_created=timezone.now()
                )
                order_obj.save()
                for prd,qty in zip(product,quantity):
                    print(prd.product_slug)
                    order_item_obj = OrderItem.objects.create(
                        order_item_id=truncate_uuid,
                        order_item_order=order_obj,
                        order_item_product=prd,
                        order_item_quantity=qty,
                        order_item_price=prd.product_price,
                        order_item_total=float(total),
                        order_item_created=timezone.now()
                    )
                    order_item_obj.save()

            messages.success(request, 'Order added successfully')
            return redirect('point_of_sales', store_slug=store_slug)

    context = {
        'store' : store,
        'product' : products,
    }
    return render(request, 'core/addorder.html', context)

def edit_orderitem(request, store_slug, product_slug):
    store = get_object_or_404(Store, store_slug=store_slug)
    products = get_object_or_404(Product,product_slug=product_slug)

    context={

    }
    return render(request, 'core/editorder.html', context)

def delete_orderitem(request, store_slug, product_slug):
    store = get_object_or_404(Store, store_slug=store_slug)
    products = get_object_or_404(Product,product_slug=product_slug)




    return redirect('point_of_sales', store_slug=store.store_slug)

def sales(request, store_slug):
    store = get_object_or_404(Store, store_slug=store_slug)
    context = {
        'store' : store,
    }
    return render(request, 'core/sales.html', context)

def product(request, store_slug):
    store = get_object_or_404(Store, store_slug=store_slug)
    products = Product.objects.all()
    context = {
        'store' : store,
        'products' : products
    }
    return render(request, 'core/products.html', context)

def add_product(request, store_slug):
    str1 = ''.join((random.choice(string.ascii_letters) for x in range(3)))  
    str1 += ''.join((random.choice(string.digits) for x in range(3))) 
    store = get_object_or_404(Store, store_slug=store_slug)
    categories = Category.objects.filter(category_store=store)

    # for category in categories:
    #     print(category)

    if request.method == "POST" and request.FILES:
        product_name = request.POST.get('product-name')
        product_slug = request.POST.get('product-slug')
        product_description = request.POST.get('product-description')
        product_price = request.POST.get('product-price')
        product_image = request.FILES.get('product-image')
        product_category = request.POST.get('product-category')
        product_store = request.POST.get('product-store')
        product_stock = request.POST.get('product-stock')
        product_created = request.POST.get('product-created')


        print(product_name, product_slug, product_description, product_price, product_image, product_category, product_store,product_stock, product_created)


        category = Category.objects.filter(category_name=product_category)
        category_name=''
        for ctg in category:
            category_name = ctg

        product_obj = Product.objects.create(
            product_name=product_name,
            product_slug=product_slug,
            product_description=product_description,
            product_stock=product_stock,
            product_price=product_price,
            product_image=product_image,
            product_category=category_name,
            product_store=store,
            product_created=product_created,
        )
        product_obj.save()



        messages.success(request, "Successfully created a Product")
        return redirect('add_product', store_slug=store.store_slug)
    context = {
        'store' : store,
        'code' : str1 ,
        'categories': categories
    }
    return render(request, 'core/addproduct.html', context)

def edit_product(request, store_slug, product_slug):
    store = get_object_or_404(Store, store_slug=store_slug)
    product = get_object_or_404(Product, product_slug=product_slug)
    categories = Category.objects.filter(category_store=store)

    if request.method == "POST" and request.FILES:
        _product_description = request.POST.get('product-description')
        _product_price = request.POST.get('product-price')
        _product_stock = request.POST.get('product-stock')
        _product_created = request.POST.get('product-created')

        print( _product_description, _product_price,_product_stock, _product_created)

        Product.objects.filter(product_slug=product_slug).update(
            product_description=_product_description,
            product_stock=_product_stock,
            product_price=_product_price,
            product_created=_product_created,
        )

        return redirect('products', store_slug=store.store_slug)

    context = {
        'store': store,
        'product' : product,
        'categories': categories
    }
    return render(request, 'core/editproduct.html', context)

def delete_product(request, store_slug, product_slug):
    store = get_object_or_404(Store, store_slug=store_slug)
    product = get_object_or_404(Product, product_slug=product_slug)
    product.delete()
    messages.success(request, 'Product deleted successfully')

    return redirect('products', store_slug=store.store_slug)


def customers(request, store_slug):
    store = get_object_or_404(Store, store_slug=store_slug)
    context = {
        'store' : store,
    }
    return render(request, 'core/customers.html', context)

def message(request, store_slug):
    store = get_object_or_404(Store, store_slug=store_slug)
    context = {
        'store' : store,
    }
    return render(request, 'core/messages.html', context)

def settings(request):
    return render(request, 'core/settings.html')