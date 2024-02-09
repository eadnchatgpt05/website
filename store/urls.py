from django.urls import path
from . import views

urlpatterns = [
	path('',views.index,name='index'),
	path('product/<str:product_name>',views.product,name='product'),
	path('shop/',views.shop,name='shop'),
	path('contact/',views.contact,name='contact'),
	path('aboutus/',views.aboutus,name='aboutus'),
	path('test/',views.test,name='test'),
	path('purchase/',views.purchase,name='purchase'),
	path('validate/<str:product_name>',views.validate,name='validate'),	
	path('shop/<str:cat_name>',views.shopCat,name='shopCat'),
	path('shop/<str:cat_name>/<str:sub_name>',views.shopCatSub,name='shopCatSub'),	
]