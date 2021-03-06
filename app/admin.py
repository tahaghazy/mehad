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
from django.contrib.sites.models import Site
from django.contrib.sites.admin import SiteAdmin

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
        'product',
        'from2',
        'to',
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
        'user',
        'product',
        'price',
        'date',
        'id',
        'ordered'

    ]
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}

    search_fields = ['full_name','product__title']
    list_filter = [OrderTowAutocomplete]
    autocomplete_fields = ['product']

    pass


class OrderrTowAdmin(admin.ModelAdmin):

    def make_refund_accepted(self, request, object):
        object.update(label='C')
    make_refund_accepted.short_description = 'تم التسليم '
    def has_change_permission(self, request, obj=Transaction):
        return False

    search_fields =['id']
    autocomplete_fields = ['items','user']
    list_filter=['ordered','label']
    list_display = [
        'user',
        'id',
        'label',
        'ordered'

    ]
    actions = [make_refund_accepted]


class TransactionAdmin(admin.ModelAdmin):


    def has_change_permission(self, request, obj=Transaction):

        return False

    def has_delete_permission(self, request, obj=Transaction):
        return False

    def has_add_permission(self, request, obj=Transaction):
        return False
    list_display = [
        'profile',
        'amount',
        'order_id',

    ]
    search_fields = ['order_id']
class SiteeAdmin(admin.ModelAdmin):
    list_display = ('domain', 'name')

    def has_delete_permission(self, request, obj=Site):
        return False

    def has_add_permission(self, request, obj=Site):
        return False
    pass

#----------------------
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderTow, OrderTowAdmin)
admin.site.register(Orderr,OrderrTowAdmin)
admin.site.register(Transaction,TransactionAdmin)
admin.site.register(Rental,RentalAdmin)
admin.site.unregister(Site)
admin.site.register(Site,SiteeAdmin)



admin.site.unregister(Group)


#----------------------

admin.site.site_header = 'لوحة التحكم'
admin.site.site_title = 'ادارة الموقع'
admin.site.index_title =''










