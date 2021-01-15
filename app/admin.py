from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group
from django.contrib import admin
from .models import *
# Register your models here.from
from admin_auto_filters.filters import AutocompleteFilter
from django.contrib.admin.actions import delete_selected
from django.contrib.auth import get_permission_codename
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter
from django.db.models import Sum
from django.contrib import admin
from django.db.models import Sum, Avg

# Register your models here.
class ArtistFilter(AutocompleteFilter):
    title = 'المنتج المستاجر'  # display title
    field_name = 'product'
class OrderTowAutocomplete(AutocompleteFilter):
    title = 'المنتج المطلوب'  # display title
    field_name = 'product'




class ProductAdmin(admin.ModelAdmin):

    list_display = [
        'title',
        'price',
        'num_in_stock',
        'num_out_stock',

        'active',



    ]
    search_fields = ['title']
    list_filter  = ['active']



class RentalAdmin(admin.ModelAdmin):
    list_display = [
        'full_name',
        'time',
        'price',
        'active'


    ]
    list_filter = ['active']
    autocomplete_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}
    list_filter = [ArtistFilter]
    search_fields = ['product__title']
    autocomplete_fields = ['product']


class OrderTowAdmin(admin.ModelAdmin):
    list_display = [
        'full_name',
        'product',
        'time',

        'price',

        'date',
        'id',

    ]
    search_fields = ['full_name','product__title']
    list_filter = [OrderTowAutocomplete]
    autocomplete_fields = ['product']

    pass



#----------------------
admin.site.register(Product, ProductAdmin)
admin.site.register(Rental, RentalAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderTow, OrderTowAdmin)
admin.site.unregister(Group)


#----------------------

admin.site.site_header = 'لوحة التحكم'
admin.site.site_title = 'ادارة الموقع'
admin.site.index_title =''












