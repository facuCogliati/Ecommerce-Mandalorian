from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),

    path('login-register', views.session_register, name="session" ),
    path('logout-register', views.session_logOut, name="logOut" ),
    path('login-session', views.session_login, name="logIn" ),

    path('market-place', views.market, name="market"),

    path('card-items', views.card, name="card"),
    path('check-out', views.checkOut, name="checkOut"),

    path('add-card', views.addItemsCard, name="addCard"),
    # path('register-user', views.registerUser, name="register-user"),

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)