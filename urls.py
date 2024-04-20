from django.urls import path

from . import views

urlpatterns = [path("index.html", views.index, name="index"),
			path("Login.html", views.Login, name="Login"),
			path("LoginAction", views.LoginAction, name="LoginAction"),
			path("Signup.html", views.Signup, name="Signup"),
			path("SignupAction", views.SignupAction, name="SignupAction"),	    
			path("VerifierLogin.html", views.VerifierLogin, name="VerifierLogin"),
			path("VerifierLoginAction", views.VerifierLoginAction, name="VerifierLoginAction"),	  
			path("AddNotary", views.AddNotary, name="AddNotary"),
			path("AddNotaryAction", views.AddNotaryAction, name="AddNotaryAction"),
			path("DeleteNotary", views.DeleteNotary, name="DeleteNotary"),
			path("DeleteNotaryAction", views.DeleteNotaryAction, name="DeleteNotaryAction"),	  
			path("ViewNotary", views.ViewNotary, name="ViewNotary"),
			path("VerifyNotary", views.VerifyNotary, name="VerifyNotary"),
			path("VerifyNotaryAction", views.VerifyNotaryAction, name="VerifyNotaryAction"),	  
]
