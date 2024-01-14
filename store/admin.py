from django.contrib import admin

# Register your models here.
from .models import Category, Subcategory, Product , Promotion , Product_Page_Left , Product_Page_Down
from .models import Index_Page_UP , ScaledImage
from .models import Wilaya , Commune , Client , Category_Acceuil, ScaledImage


admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Product)
admin.site.register(Product_Page_Down)
admin.site.register(Index_Page_UP)
admin.site.register(Category_Acceuil)
admin.site.register(ScaledImage)


class Admin_limit_0(admin.ModelAdmin):
	def has_add_permission(self, request):
		num_objects = self.model.objects.count()
		if num_objects >= 0:
		  return False
		else:
		  return True


admin.site.register(Client,Admin_limit_0)


class CommuneAdmin(admin.ModelAdmin):
    list_display = ('name', 'wilaya')
    search_fields = ['name']
	
admin.site.register(Commune, CommuneAdmin)

class WilayaAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_livraison_domicile','price_livraison_desk')
    search_fields = ['name']
	
admin.site.register(Wilaya, WilayaAdmin)


class Admin_limit_1(admin.ModelAdmin):
	def has_add_permission(self, request):
		num_objects = self.model.objects.count()
		if num_objects >= 1:
		  return False
		else:
		  return True


admin.site.register(Promotion,Admin_limit_1)

class Admin_limit_5(admin.ModelAdmin):
	def has_add_permission(self, request):
		num_objects = self.model.objects.count()
		if num_objects >= 5:
		  return False
		else:
		  return True


admin.site.register(Product_Page_Left,Admin_limit_5)



