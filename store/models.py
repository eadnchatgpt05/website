from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Category_Acceuil (models.Model):
    name = models.CharField(max_length=100)
    image_0 = models.ImageField(upload_to='products/images/list/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Product(models.Model):
    pixel = models.CharField(max_length=2000,blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_0 = models.ImageField(upload_to='products/images/list/')
    image_1 = models.ImageField(upload_to='products/images/list/')
    image_2 = models.ImageField(upload_to='products/images/list/')
    image_3 = models.ImageField(upload_to='products/images/list/',blank=True, null=True)
    image_4 = models.ImageField(upload_to='products/images/list/',blank=True, null=True)
    image_5 = models.ImageField(upload_to='products/images/list/',blank=True, null=True)
    image_6 = models.ImageField(upload_to='products/images/list/',blank=True, null=True)
    image_7 = models.ImageField(upload_to='products/images/list/',blank=True, null=True)
    image_8 = models.ImageField(upload_to='products/images/list/',blank=True, null=True)
    image_9 = models.ImageField(upload_to='products/images/list/',blank=True, null=True)
    image_10 = models.ImageField(upload_to='products/images/list/',blank=True, null=True)
    new = models.BooleanField(default = False)
    promotion = models.PositiveIntegerField(null=True,blank=True,default=0)
    promotion_prix = models.FloatField(blank=True,null=True,default=0)
    small_description = models.TextField(blank=True)
    desc_specifications = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Check if the instance is being updated (it has a primary key)
        if self.pk:
            old_instance = Product.objects.get(pk=self.pk)

            images = [
                self.image_0,
                self.image_1,
                self.image_2,
                self.image_3,
                self.image_4,
                self.image_5,
                self.image_6,
                self.image_7,
                self.image_8,
                self.image_9,
                self.image_10,
            ]

            old_images = [
                old_instance.image_0,
                old_instance.image_1,
                old_instance.image_2,
                old_instance.image_3,
                old_instance.image_4,
                old_instance.image_5,
                old_instance.image_6,
                old_instance.image_7,
                old_instance.image_8,
                old_instance.image_9,
                old_instance.image_10,
            ]

            for i in range(len(images)):
                try:
                    if images[i] != old_images[i]:
                        if(old_images[i].name == "" and images[i] != ""):
                            from PIL import Image
                            from io import BytesIO

                            img = Image.open(images[i])
                            img = img.convert('RGB')
                            img.thumbnail((100, 100)) 

                            output = BytesIO()
                            img.save(output, format='JPEG')
                            output.seek(0)

                            scaled_image = ScaledImage()
                            scaled_image.original_image = old_instance
                            
                            scaled_image.scaled_image_100x100.save(f"scaled_100x100_{images[i].name}", content=output)
                        
                            img = Image.open(images[i])
                            img = img.convert('RGB')
                            basewidth = 510
                            wpercent = (basewidth/float(img.size[0]))
                            hsize = int((float(img.size[1])*float(wpercent)))
                            img = img.resize((basewidth,hsize), Image.Resampling.LANCZOS) 

                            output = BytesIO()
                            img.save(output, format='JPEG')
                            output.seek(0)
                            scaled_image.scaled_image_510xH.save(f"scaled_510xH_{images[i].name}", content=output)
                            

                            img = Image.open(images[i])
                            img = img.convert('RGB')
                            desired_height = 296
                            hpercent = (desired_height / float(img.size[1]))
                            wsize = int((float(img.size[0]) * float(hpercent)))
                            img = img.resize((wsize, desired_height), Image.LANCZOS)

                            per_side = (int((wsize-247)/2))
                            right = per_side
                            left = per_side + (wsize-247)%2

                            left_crop = left
                            top_crop = 0
                            right_crop = wsize - right 
                            bottom_crop = desired_height

                            img = img.crop((left_crop, top_crop, right_crop, bottom_crop))


                            output = BytesIO()
                            img.save(output, format='JPEG')
                            output.seek(0)
                            scaled_image.scaled_image_247x296.save(f"scaled_247x296_{images[i].name}", content=output)


                            scaled_image.save()

                        else:
                            if(old_images[i].name != "" and images[i] == ""):
                                scaled_image = ScaledImage.objects.filter(original_image=self)
                                print(scaled_image[i])
                                scaled_image[i].delete()
                            else:
                                from PIL import Image
                                from io import BytesIO

                                img = Image.open(images[i])
                                img = img.convert('RGB')
                                img.thumbnail((100, 100)) 

                                output = BytesIO()
                                img.save(output, format='JPEG')
                                output.seek(0)
                                scaled_image = ScaledImage.objects.filter(original_image=self)
                    
                    
                                scaled_image[i].scaled_image_100x100.save(f"scaled_100x100_{images[i].name}", content=output)
                                

                                img = Image.open(images[i])
                                img = img.convert('RGB')
                                basewidth = 510
                                wpercent = (basewidth/float(img.size[0]))
                                hsize = int((float(img.size[1])*float(wpercent)))
                                img = img.resize((basewidth,hsize), Image.Resampling.LANCZOS) 

                                output = BytesIO()
                                img.save(output, format='JPEG')
                                output.seek(0)
                                scaled_image[i].scaled_image_510xH.save(f"scaled_510xH_{images[i].name}", content=output)
                                

                                img = Image.open(images[i])
                                img = img.convert('RGB')
                                desired_height = 296
                                hpercent = (desired_height / float(img.size[1]))
                                wsize = int((float(img.size[0]) * float(hpercent)))
                                img = img.resize((wsize, desired_height), Image.LANCZOS)

                                per_side = (int((wsize-247)/2))
                                right = per_side
                                left = per_side + (wsize-247)%2

                                left_crop = left
                                top_crop = 0
                                right_crop = wsize - right 
                                bottom_crop = desired_height

                                img = img.crop((left_crop, top_crop, right_crop, bottom_crop))


                                output = BytesIO()
                                img.save(output, format='JPEG')
                                output.seek(0)
                                scaled_image[i].scaled_image_247x296.save(f"scaled_247x296_{images[i].name}", content=output)

                                scaled_image[i].save()


                        
                    
                        
                except Exception as e:
                    print(e)
                    pass

                
                

        super().save(*args, **kwargs)

class ScaledImage(models.Model):
    original_image = models.ForeignKey(Product, on_delete=models.CASCADE)
    scaled_image_100x100 = models.ImageField(upload_to='scaled_images_100x100/',default="")
    scaled_image_510xH = models.ImageField(upload_to='scaled_images_510xH/',default="")
    scaled_image_247x296 = models.ImageField(upload_to='scaled_images_247x296/',default="")


class Promotion(models.Model):
    promo = models.DateTimeField()


class Product_Page_Left(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name

class Product_Page_Down(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name

class Index_Page_UP(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name

class Wilaya(models.Model):
    name = models.CharField(max_length=200)
    price_livraison_domicile = models.FloatField(default=0)
    price_livraison_desk = models.FloatField(default=0)

    def __str__(self):
        return self.name

class Commune(models.Model):
    name = models.CharField(max_length=200)
    wilaya = models.ForeignKey(Wilaya, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class Client(models.Model):
    fname = models.CharField(max_length=200)
    lname = models.CharField(max_length=200)
    wilaya = models.CharField(max_length=200)
    commune = models.CharField(max_length=200)
    adresse = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    produit = models.CharField(max_length=200,blank=True)
    qte = models.CharField(max_length=200,blank=True)
    prix = models.CharField(max_length=200,blank=True)


    
    def __str__(self):
        return "{0} {1}".format(self.fname,self.lname)
