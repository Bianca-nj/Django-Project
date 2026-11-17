from pyexpat.errors import messages

from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout

from patient.forms import PatientForm
from patient.models import Patient, Payment
from patient.serializers import PatientSerializer
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from django.contrib import messages
from django_daraja.mpesa.core import MpesaClient


# Create your views here.
def index(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('dashboard')
    else:
            form = UserCreationForm()
    return render(request,'index.html',{'form': form})

def userlogin(request):
    if request.method == 'POST':
       username = request.POST.get('username')
       password = request.POST.get('password')
       user = authenticate(request, username=username, password=password)
       if user is not None:
           login(request, user)
           return redirect('dashboard')
       else:
             error_message = 'Invalid username or password'
             return render(request, 'login.html', {'error': error_message})
    return render(request, 'login.html')

@login_required
def dashboard(request):
    patients = Patient.objects.all()

    patient_forms = [
        (patient, PatientForm(instance=patient))
        for patient in patients
    ]

    add_form = PatientForm()

    return render(request, 'dashboard.html', {
        'patients': patients,
        'patient_forms': patient_forms,
        'add_form': add_form
    })

@login_required
def profile(request):
    return render(request, 'Profile.html')

@login_required
def appointment(request):
    return render(request,'bookappointment.html')

@login_required
def logout_view(request):
    auth_logout(request)
    return redirect('login')

def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = PatientForm()
    return render(request, 'add_patient.html', {'form': form})

@login_required
def edit_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)

        if form.is_valid():
            form.save()
            return redirect('dashboard')

    return redirect('dashboard')

@login_required
def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    return render(request, 'patient_detail.html', 
                  {'patient': patient})

@login_required
def delete_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        patient.delete()
        return redirect('dashboard')
    return render(request, 'delete_patient.html', {'patient': patient})

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [AllowAny] 

@login_required
def make_payment(request):
    if request.method == 'POST':
        patient_name = request.POST.get('patient_name')
        phone_number = request.POST.get('phone_number')
        amount = int(request.POST.get('amount'))

        payment = Payment.objects.create(
            patient_name=patient_name,
            phone_number=phone_number,
            amount=amount
        )
        client = MpesaClient()
        account_reference = "Hospital Payment"
        transaction_desc = "Payment for hospital services"
        callback_url = "https://darajambili.herokuapp.com/express-payment"  # Replace with your callback URL
        response = client.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
        print(response.text)
        payment.transaction_id = response.checkout_request_id
        payment.save()
        messages.success(request, 'Payment initiated successfully. Please complete the payment on your phone.')


        return redirect('dashboard')
    return render(request, 'make_payment.html')