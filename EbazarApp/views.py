from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from .models import Product,Contact,Order,OrderUpdate,ProductType
from math import ceil
import random,string,json
from django.contrib.auth import authenticate,login,logout 
from django.contrib import messages 
from django.contrib.auth.models import User 

# Create your views here.

def home(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    
    #fetching types
    prod_types=ProductType.objects.all()
    params = {'allProds':allProds,'prod_types':prod_types}
    return render(request,'EbazarApp/homePage.html',params)

def about(request):
    return render(request,'EbazarApp/about.html')

def contact(request):
    if request.method=="POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
    return render(request, 'EbazarApp/contact.html')

def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Order.objects.filter(order_id_str=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id_str=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps([updates, order[0].items_json], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, 'EbazarApp/tracker.html')

def search(request):
    return HttpResponse("We are at search")

def productView(request, myid):
    product=Product.objects.filter(id=myid)
    print(product)
    return render(request, "EbazarApp/prodView.html", {'product':product[0]})

def checkout(request):
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')

        ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 6))   
        order_id_str=str(ran)
        
        order = Order(order_owner=request.user,order_id_str=order_id_str,items_json=items_json, name=name, 
        email=email, address=address, city=city,zip_code=zip_code, phone=phone)
        order.save()
        update = OrderUpdate(order_id_str=order.order_id_str, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id_str
        messages.success(request,"order has been placed.")
        return render(request, 'EbazarApp/checkout.html', {'thank':thank, 'id': id})
    return render(request, 'EbazarApp/checkout.html')


def products_view(request,type_name):
    type=ProductType.objects.get(type_name=type_name)
    products=Product.objects.filter(category=type)
    params={"products":products}
    return render(request,'EbazarApp/productsView.html',params)
#signup page
def signup(request):
    return render(request,'EbazarApp/signup.html')

def login_page(request):
    return render(request,'EbazarApp/login.html')
#handle signup
def handleSignUp(request):
    if request.method=='POST':
        # Get the post parameters
        username=request.POST['user-name']
        email=request.POST['email']
        fname=request.POST['fname']
        lname=request.POST['lname']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        reg="registration"
        #user=User()

        # check for errorneous input

        if len(username)>10:
            messages.error(request, " Your user name must be under 10 characters")
            return redirect('homepage')

        if not username.isalnum():
            messages.error(request, " User name should only contain letters and numbers")
            return redirect('homepage')
        if (pass1!= pass2):
             messages.error(request, " Passwords do not match")
             return redirect('homepage')
            # Create the user 
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name= fname
        myuser.last_name= lname
        myuser.save() 

        messages.success(request,"signUp successful")
        return redirect('home')
    else:
        return HttpResponse("404 - Not found")

# handle login login 
def handleLogIn(request):
    if request.method=='POST':
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpass']
        user=authenticate(request,username=loginusername,password=loginpassword)
        if user is not None:
            login(request,user)
            messages.success(request,"successfully logged in")
            return redirect('home')
        else:
            messages.error(request,'User not found')
            return redirect('home')
    return HttpResponse("404 - Not found!!!")

    
#handle logout
def handleLogOut(request):
    logout(request)
    messages.success(request,'successfully loged out')
    return redirect('home')


def handleOrders(request):
    orders=Order.objects.filter(order_owner=request.user)
    params={"orders":orders}
    return render(request,'EbazarApp/orders.html',params)