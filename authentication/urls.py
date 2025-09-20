from django.urls import path, include
from authentication import views

urlpatterns = [
    # LOGIN
    path('login/', views.login_view, name="login_view"),

    # FORGOT PASSWORD
    path('forgot_password/', views.forgot_password, name="forgot_password"),
    path('fetch_email/', views.fetch_email, name="fetch_email"),
    path('reset_password/', views.reset_password, name="reset_password"),
    
    # SIGNUP PROCESS
    path('email_verification',views.email_verification, name="email_verification"),
    path('upload_document',views.upload_document, name="upload_document"),
    path('user_details', views.user_details, name= 'user_details'),
    path('signup_data', views.signup_data, name= 'signup_data'),
    path('save_signup', views.save_signup, name= 'save_signup'),

    # AFTER ACCOUNT CREATION
    path('home_page', views.home, name = 'home_page'),
    
    # MANUAL VERIFICATION
    path('manual_verification', views.manual_verification, name = "manual_verification")
]
