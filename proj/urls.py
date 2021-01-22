"""proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path ,include
from app.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url
from app.sitemaps import StaticViewSitemap ,PostSitemap
from django.contrib.sitemaps.views import sitemap
sitemaps = {
    'static': StaticViewSitemap,
    'post': PostSitemap
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('detail/<str:slug>/', detail, name='detail'),
    path('pdf/<str:pk>',pdf,name = 'pdf'),
    path('searchposts/', searchposts, name='searchposts'),
    path('process-payment/', process_payment, name='process_payment'),
    path('payment-done/', payment_canceled, name='payment_cancelled'),
    path('register/', register, name='register'),
    path('accounts/login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('cart/', OrderSummaryView.as_view(), name='order-summary'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,name='remove-single-item-from-cart'),
    path('remove-time-from-cart/<slug>/', remove_single_time_from_cart, name='remove-single-time-from-cart'),
    path('time-from-cart/<slug>/', single_time_from_cart,name='single-time-from-cart'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('checkot/', checkout, name='checkot'),
    url(r'^update-transaction/(?P<token>[-\w]+)/$', update_transaction_records,name='update_records'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name="sitemap"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
