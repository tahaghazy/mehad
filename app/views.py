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
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, View
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect
from django.utils import timezone
import uuid
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .extras import generate_order_id, transact, generate_client_token

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
        'title': 'MehadYanbu | مهاد ينبع',
        'products': products,
        'page': page,

    }
    return render(request, 'home.html', context)

def detail(request,slug):
    product = get_object_or_404(Product,slug=slug)
    return render(request, 'detail.html', context={'title':product.title,'product':product})


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_item, created = OrderTow.objects.get_or_create(
        product=item,
        user=request.user,
        ordered=False
    )
    order_qs = Orderr.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            for i in Orderr.objects.all():
                i.save()
            messages.info(request, "تم تحديث الكميه ")
            return redirect("order-summary")
        else:
            order.items.add(order_item)
            for i in Orderr.objects.all():
                i.save()
            messages.info(request, "تم اضافة العنصر للسله")
            return redirect("order-summary")
    else:
        ordered_date = timezone.now()
        a = uuid.uuid1()
        order = Orderr.objects.create(
            user=request.user, ordered_date=ordered_date,id = generate_order_id())
        order.items.add(order_item)
        for i in Orderr.objects.all():
            i.save()
        messages.info(request, "تم اضافة العنصر للسله")
    return redirect("order-summary")
@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Orderr.objects.filter(
        user=request.user,
        ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(product__slug=item.slug).exists():
            order_item = OrderTow.objects.filter(
                product=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity = 1
                order_item.save()
                order.items.remove(order_item)
                for i in Orderr.objects.all():
                    i.save()
                messages.info(request, "تم اضافة العنصر للسله")
                return redirect("order-summary")
            else:
                order.items.remove(order_item)
                for i in Orderr.objects.all():
                    i.save()
            messages.info(request, "تم حذف العنصر من السله")
            return redirect("order-summary")
        else:
            # add a message saying the user dosent have an order
            messages.info(request, "المنتج لايوجد في سلتك")
            return redirect("detail", slug=slug)
    else:
        # add a message saying the user dosent have an order
        messages.info(request, "انت لا تمتلك طلب/سلتك فارغه.")
        return redirect("detail", slug=slug)
    return redirect("detail", slug=slug)
@login_required
def single_time_from_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Orderr.objects.filter(
        user=request.user,
        ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(product__slug=item.slug).exists():
            order_item = OrderTow.objects.filter(
                product=item,
                user=request.user,
                ordered=False
            )[0]
            order_item.time += 1
            order_item.save()
            for i in Orderr.objects.all():
                i.save()
            messages.info(request, "تم تحديث مدة الاستئجار")
            return redirect("order-summary")
        else:
            # add a message saying the user dosent have an order
            messages.info(request, "المنتج لايوجد في سلتك")
            return redirect("detail", slug=slug)
    else:
        # add a message saying the user dosent have an order
        messages.info(request, "انت لا تمتلك طلب")
        return redirect("detail", slug=slug)
    return redirect("detail", slug=slug)
@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Orderr.objects.filter(
        user=request.user,
        ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(product__slug=item.slug).exists():
            order_item = OrderTow.objects.filter(
                product=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                for i in Orderr.objects.all():
                    i.save()
            else:
                order.items.remove(order_item)
                for i in Orderr.objects.all():
                    i.save()
            messages.info(request, "تم تحديث مدة الاستئجار")
            return redirect("order-summary")
        else:
            # add a message saying the user dosent have an order
            messages.info(request, "المنتج لايوجد في سلتك")
            return redirect("detail", slug=slug)
    else:
        # add a message saying the user dosent have an order
        messages.info(request, "انت لا تمتلك طلب")
        return redirect("detail", slug=slug)
    return redirect("detail", slug=slug)

@login_required
def remove_single_time_from_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Orderr.objects.filter(
        user=request.user,
        ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(product__slug=item.slug).exists():
            order_item = OrderTow.objects.filter(
                product=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.time > 1:
                order_item.time -= 1
                order_item.save()
                for i in Orderr.objects.all():
                    i.save()

            else:
                order.items.remove(order_item)
                for i in Orderr.objects.all():
                    i.save()
            messages.info(request, "تم تحديث مدة الاستئجار")
            return redirect("order-summary")
        else:
            # add a message saying the user dosent have an order
            messages.info(request, "المنتج لايوجد في سلتك")
            return redirect("detail", slug=slug)
    else:
        # add a message saying the user dosent have an order
        messages.info(request, "انت لا تمتلك طلب")
        return redirect("detail", slug=slug)

    return redirect("detail", slug=slug)


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Orderr.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "انت لا تمتلك طلب")
            return redirect("/")

def pdf(request,pk):
    pdf = get_object_or_404(Rental,id = pk)
    aa = pdf.product.items.all()
    for i in OrderTow.objects.all():
        i.save()
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


    # paypal_dict = {
    #     "business": "receiver_email@example.com",
    #     "amount": str(order.price),
    #     "item_name": str(order.product.title),
    #     "invoice": str(order.id),
    #     "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
    #     "custom": str(order.full_name),  # Custom command to correlate to some function later (optional)
    #     'return_url': request.build_absolute_uri(reverse('home')),
    #     'cancel_return': request.build_absolute_uri(reverse('payment_cancelled')),
    #     "currency_code": "EUR", }
    #
    # form = PayPalPaymentsForm(initial=paypal_dict)

    return render(request, 'process_payment.html', {'title':'الدفع','order': order, 'form': form})

@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment_cancelled.html',{'title':'الانتهاء من الدفع'})


def register(request):
    if request.method == 'POST':
        form = UsercreationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            # username = form.cleaned_data['username']
            new_user.set_password(form.cleaned_data['password1'])
            new_user.save()
            # messages.success(
            #    request, 'تهانينا {} لقد تمت عملية التسجيل بنجاح.'.format(username))
            messages.success(
                request, f'congratulations {new_user} ')
            return redirect('login')
    else:
        form = UsercreationForm()
    return render(request, 'register.html', {
        'title': 'التسجيل',
        'form': form,
    })
from django.contrib.auth import login, authenticate, logout


def login_user(request):
    if request.method == 'POST':
        form = LoginForm()
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'تم تسجيل الدخول بنجاح')
            return redirect('home')


        else:
            messages.warning(
                request, 'هناك خطأ في اسم المستخدم أو كلمة المرور.')

    else:
        form = LoginForm()
    context = {
        'title': 'تسجيل الدخول',
        'form': form,

    }
    return render(request, 'login.html', context, )
def logout_user(request):
    logout(request)
    context = {
        'title': 'تسجيل الخروج',
    }
    return render(request, 'logout.html', context)


class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Orderr.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'order': order,
            }
            return render(self.request, "checkout.html", context)

        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("checkout")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Orderr.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm(self.request.POST or None,instance=order)
            print(self.request.POST)
            if form.is_valid():
                form.save()
                order.save()
                messages.info(self.request, "تم اضافة عنوان الدفع بنجاح ")
                return redirect('checkot')

                # add redirect to the selected payment option

        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("order-summary")


@login_required()
def checkout(request, **kwargs):
    client_token = generate_client_token()
    existing_order = get_object_or_404(Orderr, user=request.user,ordered = False)

    total = existing_order.get_total()
    if request.method == 'POST':

        result = transact({
            'amount': str(existing_order.get_total()),
            'payment_method_nonce': request.POST['payment_method_nonce'],
            'options': {
                "submit_for_settlement": True
            }
        })
        if result.is_success or result.transaction:
            return redirect(reverse('update_records',
                                    kwargs={
                                        'token': result.transaction.id
                                    })
                            )
        else:
            for x in result.errors.deep_errors:
                messages.info(request, x)
                return redirect(reverse('checkout'))
    context = {
        'order': existing_order,
        'client_token':client_token,
        'total':total
    }

    return render(request, 'shoppingcheckout.html', context)



@login_required()
def update_transaction_records(request,token):
    # get the order being processed
    order_to_purchase = get_object_or_404(Orderr,user=request.user,ordered=False)
    order_to_purchas = order_to_purchase.items.all()

    # update the placed order
    for a in order_to_purchas:
        a.ordered = True
        a.product.num_in_stock -= a.quantity
        a.product.num_out_stock += a.quantity
        a.product.save()
        a.save()

    order_to_purchase.ordered = True
    order_to_purchase.label = 'B'
    order_to_purchase.save()
    transaction = Transaction(profile=request.user,
                              token=token,
                              order_id=order_to_purchase.id,
                              amount=order_to_purchase.get_total(),
                              success=True)
    # save the transcation (otherwise doesn't exist)
    transaction.save()

    # get all items in the order - generates a queryset

    messages.info(request, "تم الدفع وتأكيد الطلب بنجاح")
    return redirect(reverse('home'))
