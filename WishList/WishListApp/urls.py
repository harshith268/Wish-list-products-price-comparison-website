from django.urls import path

from . import views

urlpatterns = [path("index.html", views.index, name="index"),
	       path('Login.html', views.Login, name="Login"), 
	       path('Register.html', views.Register, name="Register"),
	       path('Signup', views.Signup, name="Signup"),
	       path('UserLogin', views.UserLogin, name="UserLogin"),
	       path('Aboutus.html', views.Aboutus, name="Aboutus"),
	       path('SearchProduct.html', views.SearchProduct, name="SearchProduct"),
	       path('SearchProductAction', views.SearchProductAction, name="SearchProductAction"),
	       
]
