from django.shortcuts import render , redirect,HttpResponseRedirect
from django.http import HttpResponse
from .models.product import Product,Category
from .models.customer import Customer
from .models.orders import Order
from store.middlewares.auth import auth_middleware
from django.utils.decorators import method_decorator

from django.contrib.auth.hashers import make_password,check_password
from django.views import View

# Create your views here.
class Index(View):
    def get(self,request):
        cart = request.session.get('cart')
        if not cart:
            request.session['cart']={}
        products = None
        categorys = Category.get_all_categories()
        categoryID = request.GET.get('category')
        if categoryID:
            products = Product.get_all_product_by_id(categoryID)
        else:
            products = Product.get_all_product()
        data = {}
        data['products'] =  products
        data['categorys'] = categorys
        return render(request, 'index.html', data)

    def post(self,request):
        product = request.POST.get('product')
        cart = request.session.get('cart')
        remove = request.POST.get('remove')
        if cart:
            quantity=cart.get(product)
            if quantity:
                if remove:
                    if quantity <=1:
                        cart.pop(product)
                    else:

                        cart[product] = quantity-1
                else:
                    cart[product] = quantity+1


            else:
                cart[product] = 1
        else:
            cart={}
            cart[product] = 1

        request.session['cart'] = cart
        return redirect('homepage')




class Signup(View):
        def get(self,request):
            return render(request,'signup.html')
        
        def post(self,request):
            postdata= request.POST
            first_name = postdata.get('first_name')
            last_name=postdata.get('last_name')
            phone=postdata.get('phone')
            email=postdata.get('email')
            password=postdata.get('password')
            # validation
            error_mesaage=None
            value = {'first_name' : first_name,
                                'last_name':last_name,
                                    'phone' : phone,
                                    'email':email

            }
            error_mesaage = None

            customer = Customer(first_name = first_name,
                                last_name=last_name,
                                    phone = phone,
                                    email=email,
                                    password= password
                )
            error_mesaage = self.velidateCustomer(customer)
            if not error_mesaage:            
                # customer.save()
                customer.password = make_password(customer.password)
                customer.register()
                return redirect('homepage')
            else:
                data = {
                'error': error_mesaage,
                'value':value
                }
                return render(request,"signup.html",data)

        def velidateCustomer(self,customer):

            error_mesaage=None

            if not customer.first_name:
                error_mesaage = " first name required"
            elif len(customer.first_name)<4:
                error_mesaage = 'first name should be greter than 4 char'
            elif not customer.last_name:
                error_mesaage = "last anme required"
            elif len(customer.last_name)<4:
                error_mesaage = "last name should be greter than 4 char"
            elif not customer.phone:
                error_mesaage = "phoneno required"
            elif len(customer.phone) <10:
                error_mesaage= "phone no should be 10 char long"
            elif not customer.email:
                error_mesaage= "email required"
            elif len(customer.email)<5:
                error_mesaage = "email must be 5 char long"
            elif customer.isExist():
                error_mesaage='Emailregistered alredy resistered'

            elif len(customer.password)<6:
                error_mesaage="pasword must be greter than 6 char"          
            return error_mesaage



class Login(View):
    return_url='None'

    def get(self,request):
        Login.return_url=request.GET.get('return_url')
        return render(request,'login.html')

    def post(self,request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag=check_password(password, customer.password)
            if flag :

                request.session['customer_id'] = customer.id
                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url=None

                    return redirect('homepage')
            else:
                error_message = 'Email or password invalid'
        else:
                error_message = 'Email or password invalid'

        return render(request,"login.html",{'error': error_message})

def logout(request):
    request.session.clear()
    return redirect('login')


class Cart(View):
    def get(self,request):
        ids = list(request.session.get('cart').keys())
        products = Product.get_product_by_id(ids)
        return render(request,'cart.html',{'products':products})

class CheckOut(View):
    def post(self,request):
        adress = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer_id')
        cart = request.session.get('cart')
        products= Product.get_product_by_id(list(cart.keys()))
        print(adress,phone,customer,cart,products)

        for product in products:
            order = Order(customer = Customer(id = customer),
            product = product,
            price = product.price,
            adress = adress,
            phone = phone,
            quantity = cart.get(str(product.id))
            )
        order.placeOrder()
        request.session['cart']= {}
        return redirect('cart')

class OrderView(View):
    
    def get(self,request):
        customer = request.session.get('customer_id')
        print(customer)
        orders = Order.get_order_by_customer(customer)
        orders.reverse()
        return render(request,'orders.html',{'orders':orders})
