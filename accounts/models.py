from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

#class UserProfileManager(models.Manager):
	#def get_queryset(self):
		#return super(UserProfileManager,self).get_queryset().filter(city='Agra')
class UserProfile(models.Model):
	#on_delete==models.DO_NOTHING,
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	description=models.CharField(max_length=100,default='')
	city=models.CharField(max_length=100,default='')
	website=models.URLField(default='')
	phone=models.IntegerField(default=0)
	#image=models.ImageField(upload_to='profile_image', blank=True)



	def __str__(self):
		return self.user.username


def create_profile(sender, **kwargs):
	if kwargs['created']:
		user_profile=UserProfile.objects.create(user=kwargs['instance'])
post_save.connect(create_profile,sender=User)




# Create your models here.
class Post(models.Model):
	post=models.CharField(max_length=500)
	translated_post = models.CharField(max_length=500,default="")
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	postImg=models.ImageField(upload_to='account', blank=True, null=True)
	postVid=models.FileField(upload_to='account', blank=True, null=True)
	created=models.DateTimeField(auto_now_add=True)
	update=models.DateTimeField(auto_now=True)


from tinymce.models import HTMLField

class MyModel(models.Model):
    content = HTMLField()
