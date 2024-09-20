from django.urls import path
from . import views

app_name = "Payment"

urlpatterns=[
    path("checkout/",views.index,name="index"),
    path("payment/",views.pay,name="payment_init"),
    path("paymentreturn/",views.payment_return,name="paymentreturn")
]