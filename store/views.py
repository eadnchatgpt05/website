from django.shortcuts import render
from .models import Product , ScaledImage , Promotion , Product_Page_Left , Product_Page_Down , Index_Page_UP , Wilaya , Commune , Client
from .models import Category , Subcategory , Category_Acceuil
import random
import os

# Create your views here.
# Create your views here.
def index(request):
    objects = Promotion.objects.all()
    index_top = Index_Page_UP.objects.all()

    IT_Selected_Name = [ p.product.name for p in Index_Page_UP.objects.all() ]
    IT_Selected = Product.objects.filter(name__in=IT_Selected_Name)

    IT_Selected_List = [ p for p in IT_Selected]

    #original_image
    for i in range(len(IT_Selected_List)):
    	thumbnails = ScaledImage.objects.filter(original_image = IT_Selected_List[i])
    	IT_Selected_List[i] = [ IT_Selected_List[i] , thumbnails[0].scaled_image_247x296.url ,
    	thumbnails[1].scaled_image_247x296.url]
    	

    Promo_List = Product.objects.exclude(promotion=0)
    Promo_List = [p for p in Promo_List]

    for i in range(len(Promo_List)):
    	thumbnails = ScaledImage.objects.filter(original_image = Promo_List[i])
    	Promo_List[i] = [ Promo_List[i] , thumbnails[0].scaled_image_247x296.url ,
    	thumbnails[1].scaled_image_247x296.url]

    
    context = {
        'objects': objects,
        'IT' : IT_Selected_List,
        'IT_Promo' : Promo_List,
        "Acceuil" : Category_Acceuil.objects.all(),
    }

   
    return render(request,"store/index.html",context)

def product(request,product_name):
	product_name = product_name.replace("-"," ")
	product = Product.objects.get(name=product_name)
	thumbnails_queryset = ScaledImage.objects.filter(original_image=product)
	prix = "{0:.3f},00".format(int(product.price)/1000)
	try:
		prix_prom = "{0:.3f},00".format(int(product.promotion_prix)/1000)
	except:
		prix_prom = 0 


	#Left Page (Only in PC)
	PL_Selected_Name = [ p.product.name for p in Product_Page_Left.objects.all() ]
	PL_Selected = Product.objects.filter(name__in=PL_Selected_Name)
	PL_Selected = [p for p in PL_Selected]

	PL_Random = Product.objects.order_by('?')
	PL_Random_Filtred = [item for item in PL_Random if item not in PL_Selected]
	PL_Random_Filtred = [p for p in PL_Random_Filtred]
	PL_Random_Filtred = PL_Random_Filtred[0:5-len(PL_Selected)]

	PL_Selected.extend(PL_Random_Filtred)


	#Down Page (PC and Phone)
	PD_Selected_Name = [ p.product.name for p in Product_Page_Down.objects.all() ]
	PD_Selected = Product.objects.filter(name__in=PD_Selected_Name)
	PD_Selected = [p for p in PD_Selected]

	PD_Random = Product.objects.order_by('?')
	PD_Random_Filtred = [item for item in PD_Random if item not in PD_Selected]
	PD_Random_Filtred = [p for p in PD_Random_Filtred]
	PD_Random_Filtred = PD_Random_Filtred[0:6-len(PD_Selected)]

	PD_Selected.extend(PD_Random_Filtred)

	SmallD = processText2(product.small_description)
	
	val = processImages(product,thumbnails_queryset)
	for v in val:
		print(v)
		print()

	context = {
		"Product":product,
		"thumbnails":processImages(product,thumbnails_queryset),
		"prix":prix,
		"prix_prom":prix_prom,
		"PL":PL_Selected,
		"PD":PD_Selected,
		"Description":processText(product.desc_specifications),
		"SmallD": SmallD,
	}

	return render(request,"store/product.html",context)


def processDesc(desc):
	arr = desc.split("\n")
	if(arr == ['']):
		arr = []
	return arr 

def processImages(product,thumbnails_queryset):

	reel_images = [
		product.image_0,
		product.image_1,
		product.image_2,
		product.image_3,
		product.image_4,
		product.image_5,
		product.image_6,
		product.image_7,
		product.image_8,
		product.image_9,
		product.image_10,
	]

	
	zipped = []

	for i in range(len(reel_images)):
		
		for j in range(len(thumbnails_queryset)):
			th = thumbnails_queryset[j].scaled_image_100x100.name.split("/")[-1].replace("scaled_100x100_","")
			im = reel_images[i].name.split("/")[-1]
			print(im,th)
			if(th == im):
				zipped.append([	
				reel_images[i],
				thumbnails_queryset[j].scaled_image_100x100,
				thumbnails_queryset[j].scaled_image_510xH,
				thumbnails_queryset[j].scaled_image_247x296
			])

	return zipped


def processText(text):
	text_splited = text.split("\n")

	gen = ""
	for t in text_splited:

	  if ( t == ""):
	    gen = gen 
	  else:

	    if (t[0] == "*" and t[-2]=="*"):
	      gen = gen + "<p  style=\"font-size:25px; margin-top: 20px;margin-bottom: 0px;\"><strong>{0}</strong></p>".format(t[1:-2]) 
	    else:
	      if(t[0] == "-"):
	        gen = gen + "<p style = \"margin-top: 5px;margin-bottom: 5px;\"><ul style = \"padding-right: 40px;margin-top: 16px;\"><li><p style = \"margin-top: 5px;margin-bottom: 5px;\">{0}</p></li></ul><p>".format(t[1:])
	      else:
	        gen = gen + "<p style = \"margin-top: 5px;margin-bottom: 5px;\">" + t + "</p>"
	return gen

def processText2(text):
	text_splited = text.split("\n")

	gen = "<p style = \"margin-top: 5px;margin-bottom: 50px;\">"
	for t in text_splited:
	  if ( t == ""):
	    gen = gen 
	  else:
	    gen = gen + t + "<br>"
	gen = gen + "</p>"
	return gen

import json

def test(request):
	w = Wilaya.objects.all()
	c = Commune.objects.all()
	

	wilaya_name = "Alger"  
	CommunesAlger = Commune.objects.filter(wilaya__name=wilaya_name)

	data = {}
	temp = []

	for wil in w :
		qs = Commune.objects.filter(wilaya=wil).values_list('name', flat=True)
		communes = [c for c in qs]
		data[wil.name] = [communes,10,15]



	data = json.dumps(data)

	context = {
		"data" : data,
		"wilaya" : w ,
		"communesAlger" : CommunesAlger
	}
	return render(request, 'store/test.html',context)
def purchase(request):

	# Print form data
	try:
		nomPro = request.POST["nameP"]
	except Exception as e:
		return render(request, 'store/404.html')

	
	prixPro = request.POST["prix"]
	qtePro = request.POST["quantity"]
	
	pixel =  request.POST["pixelProd"]
	

	w = Wilaya.objects.all()
	c = Commune.objects.all()
	

	wilaya_name = "Alger"  
	CommunesAlger = Commune.objects.filter(wilaya__name=wilaya_name)

	data = {}
	temp = []

	for wil in w :
		qs = Commune.objects.filter(wilaya=wil).values_list('name', flat=True)
		communes = [c for c in qs]
		data[wil.name] = [communes,wil.price_livraison_domicile,wil.price_livraison_desk]


	prix = float(prixPro.split(",")[0].replace(".","")) * float(qtePro)
	
	total = prix + 400 ;

	data = json.dumps(data)
	context = {
		"data" : data,
		"wilaya" : w ,
		"communesAlger" : CommunesAlger,
		"nomPro" : nomPro ,
		"prixPro" : prix ,
		"qtePro" : int(qtePro) ,
		"pixel":pixel,
		"total" : total
	}
	return render(request, 'store/purchase.html',context)

def aboutus(request):
	return render(request,"store/AboutUs.html")
def contact(request):
	return render(request,"store/contact.html")
def shop(request):
	cat = Category.objects.all()
	allSorted = []
	for c in cat:
		sb = Subcategory.objects.filter(category=c)
		allSorted.append([c,sb])


	objects = Product.objects.all()

	IT_Selected_List = [ p for p in objects]

	#original_image
	for i in range(len(IT_Selected_List)):
		thumbnails = ScaledImage.objects.filter(original_image = IT_Selected_List[i])
		IT_Selected_List[i] = [ IT_Selected_List[i] , thumbnails[0].scaled_image_247x296.url ,
		thumbnails[1].scaled_image_247x296.url]
	
	context = {
		"allSorted" : allSorted,
		'IT' : IT_Selected_List,
		"len" : len(objects),
		"NameCat" : "Shop"
	}
	

	return render(request,"store/shop.html",context)

def shopCat(request,cat_name):

	cat = Category.objects.all()
	allSorted = []
	for c in cat:
		sb = Subcategory.objects.filter(category=c)
		allSorted.append([c,sb])

	cat_name = cat_name.replace("-"," ")
	objects = Product.objects.filter(category=Category.objects.filter(name=cat_name)[0])

	IT_Selected_List = [ p for p in objects]

	#original_image
	for i in range(len(IT_Selected_List)):
		thumbnails = ScaledImage.objects.filter(original_image = IT_Selected_List[i])
		IT_Selected_List[i] = [ IT_Selected_List[i] , thumbnails[0].scaled_image_247x296.url ,
		thumbnails[1].scaled_image_247x296.url]
	
	context = {
		"allSorted" : allSorted,
		'IT' : IT_Selected_List,
		"len" : len(objects),
		"NameCat" : cat_name.replace("-"," ")
	}
	

	return render(request,"store/shop.html",context)


def shopCatSub(request,cat_name,sub_name):
	cat = Category.objects.all()
	allSorted = []
	for c in cat:
		sb = Subcategory.objects.filter(category=c)
		allSorted.append([c,sb])


	objects = Product.objects.filter(subcategory=Subcategory.objects.filter(name=sub_name.replace("-"," "))[0])

	IT_Selected_List = [ p for p in objects]

	#original_image
	for i in range(len(IT_Selected_List)):
		thumbnails = ScaledImage.objects.filter(original_image = IT_Selected_List[i])
		IT_Selected_List[i] = [ IT_Selected_List[i] , thumbnails[0].scaled_image_247x296.url ,
		thumbnails[1].scaled_image_247x296.url]
	
	context = {
		"allSorted" : allSorted,
		'IT' : IT_Selected_List,
		"len" : len(objects),
		"NameCat" : "{0} - {1}".format(cat_name.replace("-"," "),sub_name.replace("-"," "))
	}
	

	return render(request,"store/shop.html",context)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def validate(request,product_name):
	ip = get_client_ip(request)
	
	try:
		fname = request.POST["billing_first_name"]
		lname = request.POST["billing_last_name"]
		wilaya = request.POST["billing_state"]
		commune = request.POST["billing_commune"]
		city = request.POST["billing_city"]
		phone = request.POST["billing_phone"]
		prod = request.POST["nomPro"]
		quantity = request.POST["qtePro"]
		total = request.POST["hidenTotal"]

		
		new_client = Client(fname=fname,lname=lname,wilaya=wilaya,
				commune=commune,adresse=city,phone=phone,produit=prod,
				qte=quantity,prix=total)

		new_client.save()
		
	except Exception as e:
		fname = "Client"

	product_name = product_name.replace("-"," ")
	product_name = product_name.replace("%20"," ")
	print("here is : "+product_name)
	product = Product.objects.get(name=product_name)
	pixel = product.pixel

	


	return render(request,"store/validate.html",{"pixel":pixel})






















