# Create your views here.
# software piracy protection program
# users must first register using a software product DONE
# the software reads the id of the machine and generates a serial key
# the user can then login via the user id if ip is unique by providing the serial key
# the key is encrypted and is different for each machine
# after serial key is entered the software will generate a key via encryption and match with serial key of user
# if keys match the user can access software product and it doesn't match software product is locked
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import  render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.views import View
from .models import File, CustomLogin, Customer, Price, PaymentHistory
from piracyApp.forms import UserRegistrationForm, EditFileForm, CreateForm, LoginForm
import mimetypes
from ipware.ip import get_client_ip
import os
import uuid
from django.core.mail import send_mail
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import SuspiciousOperation
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from setup import settings
from django.views.generic import TemplateView
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY 


# @permission_required('auth.view_user')
def upload_file(request, id):
    instance = File.objects.get(id=id)
    form = EditFileForm(request.POST or None,request.FILES or None, instance = instance)
    if request.method == 'POST':
        # if not request.user.has_perm('auth.view_user'):
        #     raise PermissionDenied()
        title = request.POST['title']
        description = request.POST['description']
        sourceFile = request.FILES['sourceFile']
        File.objects.filter(id = id).update(title = title, description = description, sourceFile = sourceFile)
        return redirect('view')
    form = EditFileForm(instance = instance)
    return render(request, 'edit.html', {'file': instance}, {'form': form})


def register(request, **kwargs):
    form = UserRegistrationForm(request.POST)    
    if request.method == 'POST':
        request.session['email'] = request.POST['email']
        request.session['serial_key'] = request.POST.get('serial_key')
        request.session.modified = True
        customer = stripe.Customer.create(
           metadata = {
                'id': request.user.id,
                'email': request.POST["email"],
                'username': request.POST["username"],
                'ipAddr' : str(get_client_ip(request)),
                'password' : request.POST.get('password1'),
                'serial_key': request.POST.get('serial_key')
           },
           description = 'Created from Django'
        )
        if form.is_valid():
            user = form.save()
            login(request,user)
        return redirect('landing')
    context = {'form': form}
    return render(request, 'register.html', context)
 

# route for if user is authenticated and user wants to login with serial key
# after serial key is entered the software will
# generate a key via encryption and match with serial key of user

def loginWithSerialKey(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        serial_key = form.cleaned_data.get('serial_key')
        password = request.POST.get('password1')
        customer = Customer.objects.get(email=request.session['email'])
        password = check_password(password, user.password1)
        user = authenticate(serial_key=serial_key)
        if customer:
            if customer.is_active:
                login(request, customer)
                return redirect('homepage')
    form = LoginForm()
    return render(request,
                    template_name = "login.html",
                    context={"form":form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@permission_required('auth.view_user')
def create(request):
    form = CreateForm()
    if not request.user.is_superuser():
            raise PermissionDenied()
    if request.method == "POST":   
        form = CreateForm(request.POST, request.FILES)
        if form.is_valid():
            title = request.POST['title']
            description = request.POST['description']
            sourceFile = request.FILES['sourceFile']
            form = File.objects.create(title = title, description = description, sourceFile = sourceFile)
            form.save()
        user = request.user
        return redirect("homepage")
    context = {'form':form}
    return render(request,'create.html',context)    


@permission_required('auth.view_user')
def delete(request,id):
    if not request.user.is_superuser():
        raise PermissionDenied()
    data = get_object_or_404(File,id = id)
    data.delete()
    return redirect('homepage')


def homepage(request):
    email = request.session.get('email', 'abc@gmail.com')
    history = get_object_or_404(PaymentHistory, email = email)
    if history:
        Files =File.objects.all()
        serial_key = request.session.get('serial_key', uuid.uuid4())
        prices = Price.objects.all()
        context = {
            'files': Files,
            'prices': prices,
            'serial_key': serial_key

        }
        return render(request, 'download.html', context)
    else:
        return redirect('cancel')

def new_vals(request,id):
    user = request.user
    instance = File.objects.get(id=id)
    context = {
        'serial_key': user_obj.serial_key,
        'file': instance
    }
    return render_to_response('updatedview.html', context)


# Only login and redirect to download file if login is valid based on user existing with serial key
def view(request):
    user = request.user
    print(user)
    # should return username if already logged in
    if user is not None:
        return redirect('homepage')
    else:
        return redirect('login')

class HomePageView(TemplateView):
    template_name = 'landing.html'

    def get_context_data(self, **kwargs): # new
        context = super().get_context_data(**kwargs)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context

def charge(request): # new
    if request.method == 'POST':
        charge = stripe.Charge.create(
            amount=500,
            currency='usd',
            description='A Django charge',
            source=request.POST['stripeToken'],
        ),
        success_url = f'{settings.SITE_URL}/download.html'
        cancel_url = f'{settings.SITE_URL}/cancel.html'
        # return redirect('homepage')

@method_decorator(csrf_exempt, name="dispatch")
class StripeWebhookView(View):
    def post(self, request, format=None):
        payload = request.body
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = None

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        except ValueError as e:
            return HttpResponse(status = 400)
        except stripe.error.SignatureVerificationError as e:
            return HttpResponse(status = 400)
        
        if event["type"] == "checkout.session.completed":
            print("Payment Successful")
            products =File.objects.all()
            session = event["data"]["object"]
            customer_email = session["customer_details"]["email"]
            product_id = session["metadata"]["product_id"]
            product = get_object_or_404(File, id = product_id)

            PaymentHistory.objects.create(
                email = customer_email, product = product, payment_status = "completed"
            )

            return redirect('homepage')

class CancelView(TemplateView):
    template_name = "cancel.html"