from django.urls import path
from store import views
from .views import Login,Signup,Index,logout,Cart,CheckOut,OrderView
from store.middlewares.auth import auth_middleware

urlpatterns = [
    path('index/',Index.as_view(),name = 'homepage'),
    path('signup/',Signup.as_view(),name = 'signup'),
    path('login/',Login.as_view(),name = 'login'),
    path('logout/',logout, name = 'logout'),
    path('cart/',Cart.as_view(), name = 'cart'),
    path('check-out',CheckOut.as_view(), name = 'checkout'),
    path('order/',auth_middleware(OrderView.as_view), name = 'order')



]
