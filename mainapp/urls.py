from django.contrib import admin
from django.urls import path

from mainapp import views

urlpatterns = [
    path('',views.home),
    path('market/<int:categoryid>/<int:childid>/<int:opt>',views.market),
    path('cart',views.cart),
    path('mine',views.mine),
    path('regist',views.regist),
    path('login',views.login),
    path('upload',views.upload),
    path('logout',views.logout),
    path('vcode',views.vCode),
    path('select/<int:cart_id>',views.selectCart),
    path('addcart/<int:cart_id>',views.addCart),
    path('subcart/<int:cart_id>',views.subCart),
    path('order/<str:ordernum>',views.order),
    path('pay/<str:num>/<int:payType>',views.pay),
    path('orderlist/<int:state>',views.orderList),
    path('address/<int:state>/<int:id>',views.address),
    path('delcart/<int:id>',views.delcart),
    path('substores/<int:id>',views.subStores),
]
