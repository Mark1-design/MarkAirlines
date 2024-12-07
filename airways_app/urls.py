from django.urls import path
from .import views

app_name = 'airways_app'

urlpatterns = [
 path('', views.home, name='home'), 
 path('about/', views.about, name='about'),  
 path('services/', views.services, name='services'),
 path('team/', views.team, name='team'),
 path('pricing/', views.pricing, name='pricing'),
 path('booking/', views.booking, name='booking'),
 path('contact/', views.contact, name='contact'),
 path('appointment/', views.appointment, name='appointment'),
 path('show_appointments/', views.retrieve_appointments, name='show_appointments'),
 path('delete/<int:id>', views.delete_appointment, name= "delete_appointment"),
 path('edit/<int:appointment_id>/', views.update_appointment, name='update_appointment'),


 path('register/', views.register, name='register'),
 path('login/', views.login_view, name='login'),
 path('upload/', views.upload_image, name='upload_image'),

 path('pay/', views.pay, name='pay'), #view the payment form
path('stk/', views.stk, name='stk'), # Send the stk push prompt
path('token/', views.token, name='token'), #generates the token for that particular transaction
]