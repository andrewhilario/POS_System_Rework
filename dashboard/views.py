from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Store, Category, Product, Order, OrderItem

# Imports
import random
import string
from uuid import uuid4
from django.utils import timezone


def dashboard(request):
    return render(request, "core/dashboard.html")


def storelist(request):
    store = Store.objects.all()
    print(store)
    context = {
        "stores": store,
    }
    return render(request, "core/storelist.html", context)


def add_store(request):
    if request.method == "POST" and request.FILES:
        store_name = request.POST.get("store-name")
        store_address = request.POST.get("store-address")
        store_manager = request.POST.get("store-manager")
        store_image = request.FILES.get("store-image")
        store_slug = request.POST.get("store-slug")
        store_created = request.POST.get("store-created")

        print(store_name, store_address, store_manager, store_image)
        store_obj = Store.objects.create(
            store_name=store_name,
            store_address=store_address,
            store_manager=store_manager,
            store_image=store_image,
            store_slug=store_slug,
            store_created=store_created,
        )
        store_obj.save()
        messages.success(request, "Store added successfully")
        return redirect("storelist")

    return render(request, "core/addstore.html")


def pos_dashboard(request, store_slug):
    store = get_object_or_404(Store, store_slug=store_slug)
    context = {
        "store": store,
    }
    return render(request, "core/pos_dashboard.html", context)


def categories(request, store_slug):
    store = get_object_or_404(Store, store_slug=store_slug)
    categories = Category.objects.filter(category_store=store)
    context = {"store": store, "categories": categories}
    return render(request, "core/categories.html", context)


def add_category(request, store_slug):
    str1 = "".join((random.choice(string.ascii_letters) for x in range(3)))
    str1 += "".join((random.choice(string.digits) for x in range(3)))
    print(str1)
    store = get_object_or_404(Store, store_slug=store_slug)
    if request.method == "POST":
        category_name = request.POST.get("category-name")
        category_description = request.POST.get("category-description")
        category_slug = request.POST.get("category-slug")
        category_code = request.POST.get("category-code")
        category_store = request.POST.get("category-store")
        category_created = request.POST.get("category-date")

        print(
            category_name,
            category_description,
            category_slug,
            category_code,
            category_store,
            category_created,
        )

        category_obj = Category.objects.create(
            category_name=category_name,
            category_slug=category_slug,
            category_code=category_code,
            category_description=category_description,
            category_store=store,
            category_created=category_created,
        )
        category_obj.save()
        messages.success(request, "Successfully created category")
        return redirect("add_category", store_slug=store.store_slug)
    context = {"store": store, "code": str1}
    return render(request, "core/addcategory.html", context)


def edit_category(request, store_slug, category_slug):
    store = get_object_or_404(Store, store_slug=store_slug)
    category = get_object_or_404(Category, category_slug=category_slug)

    context = {"store": store, "category": category}
    return render(request, "core/editcategory.html", context)


def delete_category(request, store_slug, category_slug):
    store = get_object_or_404(Store, store_slug=store_slug)
    category = get_object_or_404(Category, category_slug=category_slug)
    category.delete()
    messages.success(request, "Category deleted successfully")

    return redirect("categories", store_slug=store.store_slug)


def pointofsales(request, store_slug):
    store = get_object_or_404(Store, store_slug=store_slug)
    products = Product.objects.filter(product_store=store)
    categories = Category.objects.filter(category_store=store)
    order = Order.objects.filter(order_store=store)
    order_items = OrderItem.objects.filter(order_item_product__product_store=store)

    order_item = OrderItem.objects.filter(
        order_item_product__product_store=store, order_item_order__order_completed=False
    )
    order_completed = False

    for ord in order:
        order_completed = ord.order_completed
    print(order_completed)

    sort = request.GET.get("sort", None)
    category = request.GET.get("filter", None)

    order_list = []
    if sort == "new":
        order_list.append("-product_created")
    elif sort == "old":
        order_list.append("product_created")
    elif sort == "price_desc":
        order_list.append("-product_price")
    elif sort == "price_asc":
        order_list.append("product_price")

    if category and category != "all":
        category = category.replace("-", " ")
        products = products.filter(product_category__category_name=category)

    if order:
        products = products.order_by(*order_list)

    category = (
        Category.objects.order_by("category_name").values("category_name").distinct()
    )

    order = Order.objects.filter(
        order_store=store, order_completed=False, order_void=False
    ).first()

    context = {
        "store": store,
        "products": products,
        "category": category,
        "order": order,
        "order_items": order_item,
        "order_completed": order_completed,
    }
    return render(request, "core/pointofsales.html", context)


def order_item(request, store_slug, product_slug):
    store = get_object_or_404(Store, store_slug=store_slug)
    products = get_object_or_404(Product, product_slug=product_slug)
    product = Product.objects.filter(product_slug=product_slug)

    uuid = uuid4()
    truncate_uuid = str(uuid)[:6]

    if request.method == "POST":
        quantity = request.POST.getlist(
            "quantity"
        )  # If multiple quantities are possible
        total = request.POST.get("total")

        if not quantity:
            messages.error(request, "Please enter a quantity")
            return redirect("pos", store_slug=store_slug)

        # Fetching any existing incomplete order
        order_obj = Order.objects.filter(
            order_completed=False, order_store=store
        ).first()

        if order_obj:
            print("Order Exists")
        else:
            print("Creating New Order")
            order_obj = Order.objects.create(
                order_id=truncate_uuid,
                order_store=store,
                order_completed=False,
                order_created=timezone.now(),
            )
            print(order_obj)
            order_obj.save()

        # Create or update the order items
        for prd, qty in zip(product, quantity):
            order_item_obj = OrderItem.objects.create(
                order_item_id=truncate_uuid,
                order_item_order=order_obj,
                order_item_product=prd,
                order_item_quantity=qty,
                order_item_price=prd.product_price,
                order_item_total=float(total),
                order_item_created=timezone.now(),
            )
            order_item_obj.save()

        messages.success(request, "Order added successfully")
        return redirect("point_of_sales", store_slug=store_slug)

    context = {
        "store": store,
        "product": products,
    }
    return render(request, "core/addorder.html", context)


def edit_orderitem(request, store_slug, product_slug):
    store = get_object_or_404(Store, store_slug=store_slug)
    products = get_object_or_404(Product, product_slug=product_slug)

    context = {}
    return render(request, "core/editorder.html", context)


def delete_orderitem(request, store_slug, product_slug):
    store = get_object_or_404(Store, store_slug=store_slug)
    products = get_object_or_404(Product, product_slug=product_slug)

    order_item = OrderItem.objects.filter(
        order_item_product__product_store=store, order_item_order__order_completed=False
    )

    for order_item in order_item:
        order_item.delete()

    order = Order.objects.filter(order_store=store, order_completed=False)
    for ord in order:
        ord.delete()

    messages.success(request, "Order deleted successfully")

    return redirect("point_of_sales", store_slug=store.store_slug)


def sales(request, store_slug):
    store = get_object_or_404(Store, store_slug=store_slug)
    context = {
        "store": store,
    }
    return render(request, "core/sales.html", context)


def product(request, store_slug):
    store = get_object_or_404(Store, store_slug=store_slug)
    products = Product.objects.all()
    context = {"store": store, "products": products}
    return render(request, "core/products.html", context)


def add_product(request, store_slug):
    str1 = "".join((random.choice(string.ascii_letters) for x in range(3)))
    str1 += "".join((random.choice(string.digits) for x in range(3)))
    store = get_object_or_404(Store, store_slug=store_slug)
    categories = Category.objects.filter(category_store=store)

    # for category in categories:
    #     print(category)

    if request.method == "POST" and request.FILES:
        product_name = request.POST.get("product-name")
        product_slug = request.POST.get("product-slug")
        product_description = request.POST.get("product-description")
        product_price = request.POST.get("product-price")
        product_image = request.FILES.get("product-image")
        product_category = request.POST.get("product-category")
        product_store = request.POST.get("product-store")
        product_stock = request.POST.get("product-stock")
        product_created = request.POST.get("product-created")

        print(
            product_name,
            product_slug,
            product_description,
            product_price,
            product_image,
            product_category,
            product_store,
            product_stock,
            product_created,
        )

        category = Category.objects.filter(category_name=product_category)
        category_name = ""
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
        return redirect("add_product", store_slug=store.store_slug)
    context = {"store": store, "code": str1, "categories": categories}
    return render(request, "core/addproduct.html", context)


def edit_product(request, store_slug, product_slug):
    store = get_object_or_404(Store, store_slug=store_slug)
    product = get_object_or_404(Product, product_slug=product_slug)
    categories = Category.objects.filter(category_store=store)

    if request.method == "POST" and request.FILES:
        _product_description = request.POST.get("product-description")
        _product_price = request.POST.get("product-price")
        _product_stock = request.POST.get("product-stock")
        _product_created = request.POST.get("product-created")

        print(_product_description, _product_price, _product_stock, _product_created)

        Product.objects.filter(product_slug=product_slug).update(
            product_description=_product_description,
            product_stock=_product_stock,
            product_price=_product_price,
            product_created=_product_created,
        )

        return redirect("products", store_slug=store.store_slug)

    context = {"store": store, "product": product, "categories": categories}
    return render(request, "core/editproduct.html", context)


def delete_product(request, store_slug, product_slug):
    store = get_object_or_404(Store, store_slug=store_slug)
    product = get_object_or_404(Product, product_slug=product_slug)
    product.delete()
    messages.success(request, "Product deleted successfully")

    return redirect("products", store_slug=store.store_slug)


def customers(request, store_slug):
    store = get_object_or_404(Store, store_slug=store_slug)
    context = {
        "store": store,
    }
    return render(request, "core/customers.html", context)


def message(request, store_slug):
    store = get_object_or_404(Store, store_slug=store_slug)
    context = {
        "store": store,
    }
    return render(request, "core/messages.html", context)


def settings(request):
    return render(request, "core/settings.html")


def show_receipt(request, order_id):
    # Get the order based on the ID
    order = get_object_or_404(Order, id=order_id)

    # Calculate total price, etc., if needed
    total_price = sum(item.order_item_total for item in order.order_items.all())  # type: ignore
    context = {"order": order, "total_price": total_price}

    return render(request, "core/receipt.html", context)
