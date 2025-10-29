from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import CustomUser, DiningTable, Category, Product, Order, OrderProduct


@admin.register(CustomUser)
class CustomUserAdmin(DjangoUserAdmin):
    # Show these columns in the user list
    list_display = ("id", "username", "name", "email", "role", "activated", "is_staff", "is_active")
    list_filter = ("role", "activated", "is_staff", "is_active")
    search_fields = ("username", "email", "name", "phone_number")
    ordering = ("-id",)

    # Add our custom fields to the standard Django user fieldsets
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("Additional info", {
            "fields": ("name", "phone_number", "role", "activated"),
        }),
    )

    # Fields shown on the "Add user" form in admin
    add_fieldsets = DjangoUserAdmin.add_fieldsets + (
        (None, {
            "classes": ("wide",),
            "fields": ("name", "email", "phone_number", "role", "activated"),
        }),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "price")
    list_filter = ("category",)
    search_fields = ("name", "category__name")
    autocomplete_fields = ("category",)


@admin.register(DiningTable)
class DiningTableAdmin(admin.ModelAdmin):
    list_display = ("id", "qr", "capacity", "is_occupied")
    list_filter = ("is_occupied",)
    search_fields = ("qr",)


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 0
    autocomplete_fields = ("product",)
    fields = ("product", "quantity", "notes")
    verbose_name = "Order item"
    verbose_name_plural = "Order items"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "table", "status", "created_at", "total_amount")
    list_filter = ("status", "table")
    search_fields = ("id", "user__username", "user__email", "user__name")
    autocomplete_fields = ("user", "table")
    readonly_fields = ("created_at", "updated_at")
    inlines = [OrderProductInline]
    date_hierarchy = "created_at"

    def get_queryset(self, request):
        # Prefetch order items and related products for efficient totals
        qs = super().get_queryset(request)
        return qs.prefetch_related("order_items__product")

    def total_amount(self, obj):
        # Compute order total in admin list view
        return sum((item.quantity or 0) * (item.product.price or 0) for item in obj.order_items.all())
    total_amount.short_description = "Total"
    total_amount.admin_order_field = None  # Not sortable since it's computed


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product", "quantity")
    list_filter = ("product",)
    search_fields = ("order__id", "product__name")
    autocomplete_fields = ("order", "product")


# Optional: Customize admin interface texts
admin.site.site_header = "Restaurant Automation Administration"
admin.site.site_title = "Restaurant Automation Admin Portal"
admin.site.index_title = "Welcome to Restaurant Automation Admin Portal"

