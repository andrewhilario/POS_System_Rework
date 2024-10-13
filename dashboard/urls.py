from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = (
    [
        path("", views.dashboard, name="dashboard"),
        path("settings", views.settings, name="settings"),
        path("store-list/", views.storelist, name="storelist"),
        path("store-list/add/", views.add_store, name="add_store"),
        path("store/<slug:store_slug>/", views.pos_dashboard, name="pos_dashboard"),
        # Categories
        path(
            "store/<slug:store_slug>/categories/", views.categories, name="categories"
        ),
        path(
            "store/<slug:store_slug>/categories/add/",
            views.add_category,
            name="add_category",
        ),
        path(
            "store/<slug:store_slug>/categories/edit/<slug:category_slug>",
            views.edit_category,
            name="edit_category",
        ),
        path(
            "store/<slug:store_slug>/categories/delete/<slug:category_slug>",
            views.delete_category,
            name="delete_category",
        ),
        # Point of Sales
        path(
            "store/<slug:store_slug>/point-of-sales/",
            views.pointofsales,
            name="point_of_sales",
        ),
        path(
            "store/<slug:store_slug>/order/<slug:product_slug>",
            views.order_item,
            name="order_item",
        ),
        path(
            "store/<slug:store_slug>/order/<slug:product_slug>/edit/",
            views.edit_orderitem,
            name="edit_orderitem",
        ),
        path(
            "store/<slug:store_slug>/order/<slug:product_slug>/delete/",
            views.delete_orderitem,
            name="delete_orderitem",
        ),
        path("store/<slug:store_slug>/sales/", views.sales, name="sales"),
        # Products
        path("store/<slug:store_slug>/products/", views.product, name="products"),
        path(
            "store/<slug:store_slug>/products/add/",
            views.add_product,
            name="add_product",
        ),
        path(
            "store/<slug:store_slug>/products/edit/<slug:product_slug>/",
            views.edit_product,
            name="edit_product",
        ),
        path(
            "store/<slug:store_slug>/products/delete/<slug:product_slug>/",
            views.delete_product,
            name="delete_product",
        ),
        # Coming Soon
        path("store/<slug:store_slug>/customers", views.customers, name="customers"),
        path("store/<slug:store_slug>/messages", views.message, name="messages"),
        path("receipt/<int:order_id>", views.show_receipt, name="show_receipt"),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)
