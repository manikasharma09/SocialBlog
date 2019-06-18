from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path,re_path, include
from djangoproject import views 
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^$',views.login_redirect, name='login_redirect'),
    url('', include('social_django.urls', namespace='social')),
    path('admin/', admin.site.urls),
    url(r'^account/',include('accounts.urls',namespace='accounts') ),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
