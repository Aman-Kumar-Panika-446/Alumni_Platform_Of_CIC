from django.urls import path
from dashboard import views

urlpatterns = [
    # SHOW THE DASHBOARD
    path('', views.dashboard, name = "dashboard"),
    
    # EDIT CURRENT STATUS
    path('edit_current_status/', views.edit_current_status, name = "edit_current_status"),
    
    # EDIT PROFILE IMAGES
    path("update_profile_pic/", views.update_profile_pic, name ="update_profile_pic" ),

    # DEALING WITH EXPERIENCE
    path('view_experience/', views.view_experience, name = "view_experience"),
    path('add_experience/', views.add_experience, name = "add_experience"),
    path('edit_experience/<int:pk>/', views.edit_experience, name = "edit_experience"),
    path('delete_experience/<int:pk>/', views.delete_experience, name = "delete_experience"),
   
    # DEALING WITH SKILLS
    path('view_skills/', views.view_skills, name = "view_skills"),
    path('add_skill/', views.add_skill, name = "add_skill"),
    path('edit_skill/<int:pk>/', views.edit_skill, name = "edit_skill"),
    path('delete_skill/<int:pk>/', views.delete_skill, name = "delete_skill"),

    # LOGOUT
    path('logout/', views.user_logout, name = "user_logout"),

]