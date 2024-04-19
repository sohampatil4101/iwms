from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('home/',views.home, name='home'),
    path('registeruser/',views.Registeruser.as_view()),
    path('loginuser/',views.LoginUser.as_view()),
    path('soham/',views.soham.as_view()),
    path('postgstdetails/',views.Postgstdetails.as_view()),
    path('postadditem/',views.Postadditem.as_view()),
    path('postinventory/',views.PostInventory.as_view()),

]

if settings.DEBUG :
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

