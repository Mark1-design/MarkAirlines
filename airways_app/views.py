from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.files.storage import FileSystemStorage
from .models import UploadedImage 

import requests
import json
from django.http import HttpResponse

from .models import Appointment
from airways_app.credentials import LipanaMpesaPpassword, MpesaAccessToken
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail
from .models import Booking

# Create your views here.
@login_required
def home(request):
    """ Display the home page"""
    return render(request, 'index.html')

@login_required
def about(request):
    """ Display the about page"""
    return render(request, 'about.html')

@login_required
def services(request):
    """ Display the services page"""
    return render(request, 'services.html')

@login_required
def team(request):
    """ Display the team page"""
    return render(request, 'team.html')

@login_required
def pricing(request):
    """ Display the pricing page"""
    return render(request, 'pricing.html')

@login_required
def contact(request):
    """ Display the contact page"""
    return render(request, 'contact.html')


@login_required(login_url='airways_app:login')
def appointment(request):
    """ Appointment booking """
    if request.method == 'POST':
        # Extract fields and validate
        
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        destination = request.POST.get('destination')
        departure_date = request.POST.get('departure_date')
        return_date = request.POST.get('return_date')
        number_of_passengers = request.POST.get('passengers')

        # Validate required fields
        if not all([name, email, subject, destination, departure_date, return_date, number_of_passengers]):
            messages.error(request, "All fields are required.")
            return redirect('airways_app:appointment')

        try:
            # Convert number_of_passengers to integer
            number_of_passengers = int(number_of_passengers)

            # Create and save the appointment
            appointment = Appointment.objects.create(
                name=name,
                email=email,
                subject=subject,
                destination=destination,
                departure_date=departure_date,
                return_date=return_date,
                number_of_passengers=number_of_passengers
            )
            appointment.save()
            messages.success(request, "Appointment booked successfully!")
            return redirect('airways_app:show_appointments')
        except ValueError:
            messages.error(request, "Invalid number of passengers.")
            return redirect('airways_app:appointment')
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect('airways_app:appointment')

    return render(request, 'appointment.html')

    
    #Retrieve all appointments

@login_required(login_url='airways_app:login')
def retrieve_appointments(request):
    """Retrieve/fetch all appointments"""
    #Create a variable to store these appointments
    user_appointments = Appointment.objects.filter(user=request.user)
    context = {
        "appointments": user_appointments
        }
    return render(request, 'show_appointments.html', context)

# Update

@login_required(login_url='airways_app:login')
def update_appointment(request, appointment_id):
    """Manually updating an existing appointment."""
    appointment = get_object_or_404(Appointment, id=appointment_id, user=request.user)  # Fetch the appointment by its ID
    
    if request.method == 'POST':
        # Use .get() to avoid KeyErrors and handle missing fields
        appointment.name = request.POST.get('name', appointment.name)
        appointment.email = request.POST.get('email', appointment.email)
        appointment.subject = request.POST.get('subject', appointment.subject)
        appointment.destination = request.POST.get('destination', appointment.destination)
        appointment.departure_date = request.POST.get('departure_date', appointment.departure_date)
        appointment.return_date = request.POST.get('return_date', appointment.return_date)
        appointment.number_of_passengers = request.POST.get('passengers', appointment.number_of_passengers)
        
        # Save the updated appointment
        try:
            appointment.save()
            messages.success(request, "Appointment updated successfully!")
            return redirect('airways_app:show_appointments')  # Redirect after successful update
        except Exception as e:
            messages.error(request, f"Error updating appointment: {e}")
    
    # If GET request, render the update page with current appointment data
    context = {
        'appointment': appointment
    }
    return render(request, 'update_appointment.html', context)


#Delete
def delete_appointment(request, id):
    """ Deleting """
    appointment = Appointment.objects.get(id=id) # fetch the particular appointment by its id
    appointment.delete()
    return redirect("airways_app:show_appointments") #just remain on the same page

# Register 

def register(request):
    """Show the registration"""
    if request.method =="POST":
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

     #Check the password
        if password == confirm_password:
            try:
                user = User.objects.create_user(username=username, password=password)
                user.save()
            
                #Display a message 
               
                messages.success(request, "Account created successfully")
                return redirect('airways_app:home')
            except:
                #Display a message if the above fails
                messages.error(request, "Username already exist")
        else:
            #Display a message saying password do not match
            messages.error(request, "Password do not match")

    return render(request, 'register.html')

def login_view(request): 
    """Login view"""
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        #Check if the user exists
        if user is not None:
            login(request, user)
            messages.success(request, "You are now logged in!")
            return redirect("airways_app:home")
        else:
            messages.error(request, "Invalid login credentials")
 
    return render(request,'login.html') 

#Image Upload
def upload_image(request):
    if request.method == 'POST':
        #Retrieve data from the form
        title = request.POST['title']
        uploaded_file = request.FILES['image'] 

        #Save the file using FileSystemStorage
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_url = fs.url(filename)

        #Save file information to the database
        image = UploadedImage.objects.create(title=title, image=filename)
        image.save()

        return render(request, 'upload_success.html', {'file_url':file_url})
    return render(request, 'upload_image.html')


@login_required
def booking(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        destination = request.POST.get('destination')
        departure_date = request.POST.get('departure_date')
        return_date = request.POST.get('return_date')
        passengers = request.POST.get('passengers')

        # Save the booking
        Booking.objects.create(
            name=name,
            destination=destination,
            departure_date=departure_date,
            return_date=return_date,
            number_of_passengers=passengers
        )
        
        messages.success(request, 'Flight booking successful!')
        return redirect('airways_app:home')  

    # If GET request, display the booking form
    return render(request, 'booking.html')  



# Adding the mpesa functions

#Display the payment form
def pay(request):
   """ Renders the form to pay """
   return render(request, 'pay.html')


# Generate the ID of the transaction
def token(request):
    """ Generates the ID of the transaction """
    consumer_key = 'l1uoggbhwWwMUUJichTqCDm95hvMNNjhyEcfKFIptNavU8VX'
    consumer_secret = 'b49gIBHmCmrJvVH8C7E5eVbVQLh6onqKNPrAFMh5JSe4daYbRxUJuX4Vu7ebQuAg'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]

    return render(request, 'token.html', {"token":validated_mpesa_access_token})


# Send the stk push
def stk(request):
    """ Sends the stk push prompt """
    if request.method =="POST":
        phone = request.POST['phone']
        amount = request.POST['amount']
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "eMobilis",
            "TransactionDesc": "Web Development Charges"
        }
        response = requests.post(api_url, json=request, headers=headers)
        return HttpResponse("Success")