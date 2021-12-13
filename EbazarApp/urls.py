
from django.urls import path,include
from . import views
from django.conf.urls import url



urlpatterns = [
     path('',views.home,name="home"),
     path('about/', views.about,name="AboutUs"),
     path('contact/', views.contact,name="ContactUs"),
     path('tracker', views.tracker,name="TrackingStatus"),
     path('search/', views.search,name="Search"),
     path("products/<int:myid>", views.productView, name="ProductView"),
     path('checkout/', views.checkout,name="Checkout"),
     path('products-view/<str:type_name>',views.products_view,name='products_view'),
     path('signup/',views.signup,name="signup"),
     path('login-page/',views.login_page,name="login"),
     path('logout/',views.handleLogOut,name="handleLogOut"),
     path('login-page/handle-login/',views.handleLogIn,name='handleLogIn'),
     path('signup/handle-signup/',views.handleSignUp,name='handleSignUp'),
     path('orders/',views.handleOrders,name="handleOrders")
] 