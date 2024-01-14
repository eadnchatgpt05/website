from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product, Promotion, ScaledImage



@receiver(post_save, sender=Product)
def scale_and_save_image(sender, instance, created, **kwargs):
    if created:  # Only run this for new instances
        # Scale the image using Pillow
        from PIL import Image
        from io import BytesIO

        images = [
            instance.image_0,
            instance.image_1,
            instance.image_2,
            instance.image_3,
            instance.image_4,
            instance.image_5,
            instance.image_6,
            instance.image_7,
            instance.image_8,
            instance.image_9,
            instance.image_10,
        ]

        # Image Type 1
        for image_ in images:
            try: 
                img = Image.open(image_)
                img = img.convert('RGB')
                img.thumbnail((100, 100)) 

                output = BytesIO()
                img.save(output, format='JPEG')
                output.seek(0)

                scaled_image = ScaledImage()
                scaled_image.original_image = instance
                scaled_image.scaled_image_100x100.save(f"scaled_100x100_{image_.name}", content=output)
                

                img = Image.open(image_)
                img = img.convert('RGB')
                basewidth = 510
                wpercent = (basewidth/float(img.size[0]))
                hsize = int((float(img.size[1])*float(wpercent)))
                img = img.resize((basewidth,hsize), Image.Resampling.LANCZOS) 

                output = BytesIO()
                img.save(output, format='JPEG')
                output.seek(0)

                scaled_image.scaled_image_510xH.save(f"scaled_510xH_{image_.name}", content=output)
                

                img = Image.open(image_)
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

                scaled_image.scaled_image_247x296.save(f"scaled_247x296_{image_.name}", content=output)
                

                scaled_image.save()

            except:
                i = 0 
