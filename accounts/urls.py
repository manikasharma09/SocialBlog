from django.conf.urls import url
from django.urls import path,re_path, include
from . import views
from accounts.views import HomeView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import (
 LoginView,LogoutView,PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView
 )
app_name="accounts"

urlpatterns = [
       url(r'^$',HomeView.as_view(),name='home'),
       path('login/', LoginView.as_view(template_name='accounts/login.html'),name='login'),
       path('logout/', LogoutView.as_view(template_name='accounts/logout.html'),name='logout'),
       url(r'authSocial', include('social_django.urls', namespace='social')),
       url(r'^STT/$',views.STT,name="STT"),
       url(r'^register/$',views.register,name="register"),
       url(r'^profile/$',views.view_profile,name="view_profile"),
       url(r'^profile/edit/$',views.edit_profile,name="edit_profile"),
       url(r'^change-password/$',views.change_password,name="change_password"),
       url(r'^reset-password/$',PasswordResetView.as_view(),name="reset_password"),
       url(r'^reset-password/done/$',PasswordResetDoneView.as_view(),name="password_reset_done"),
       url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',PasswordResetConfirmView.as_view(),name="password_reset_confirm"),
       url(r'^reset-password/complete/$',PasswordResetCompleteView.as_view(),name="password_reset_complete"),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



 