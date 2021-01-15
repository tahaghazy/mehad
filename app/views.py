from django.shortcuts import render
from .models import *
from django.shortcuts import render,get_object_or_404
from .models import *
from django.core.paginator import PageNotAnInteger,Paginator,EmptyPage
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db.models import F
from django.db.models import Count
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

def home(request):
    products = Product.objects.filter(active=True)
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_page)
    context = {
        'title': 'الصفحة الرئيسية',
        'products': products,
        'page': page,

    }
    return render(request, 'home.html', context)

def detail(request,slug):
    product = get_object_or_404(Product,slug=slug)
    if request.method == 'POST':
        comment_form = NewOrder(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.product = product

            new_comment.save()
            request.session['order_id'] = new_comment.id
            return redirect('process_payment')

    else:
        comment_form = NewOrder()


    # What you want the button to do.


    # Create the instance.

    return render(request, 'detail.html', context={'title':product.title,'product':product,'comment_form':comment_form})

def pdf(request,pk):
    pdf = get_object_or_404(Rental,id = pk)
    aa = pdf.product.all()


    return render(request,'pdf.html',context={'i':pdf,'aa':aa})


def searchposts(request):
    if request.method == 'GET':
        query= request.GET.get('q')

        submitbutton= request.GET.get('submit')

        if query is not None:
            lookups= Q(title__icontains=query) | Q(content__icontains=query)

            results= Product.objects.filter(lookups).distinct()

            context={'title':'نتائج البحث',
                'results': results,
                     'submitbutton': submitbutton}

            return render(request, 'search.html', context)

        else:
            return render(request, 'search.html')

    else:
        return render(request, 'search.html')

def process_payment(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(OrderTow, id=order_id)


    paypal_dict = {
        "business": "receiver_email@example.com",
        "amount": str(order.price),
        "item_name": str(order.product.title),
        "invoice": str(order.id),
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "custom": str(order.full_name),  # Custom command to correlate to some function later (optional)
        'return_url': request.build_absolute_uri(reverse('home')),
        'cancel_return': request.build_absolute_uri(reverse('payment_cancelled')),
        "currency_code": "EUR", }

    form = PayPalPaymentsForm(initial=paypal_dict)

    return render(request, 'process_payment.html', {'title':'الدفع','order': order, 'form': form})

@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment_cancelled.html',{'title':'الانتهاء من الدفع'})



