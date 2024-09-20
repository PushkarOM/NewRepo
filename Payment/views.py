import jsons
import base64
import requests
import shortuuid
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.shortcuts import redirect
from cryptography.hazmat.primitives import hashes
from django.views.decorators.csrf import csrf_exempt
from cryptography.hazmat.backends import default_backend
from Booking.models import *
from urllib.parse import urlencode
from django.core import signing
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from Ayojan import settings

# Create your views here.
def index(request):
    return render(request, 'Payment/checkout.html')


def calculate_sha256_string(input_string):
    # Create a hash object using the SHA-256 algorithm
    sha256 = hashes.Hash(hashes.SHA256(), backend=default_backend())
    # Update hash with the encoded string
    sha256.update(input_string.encode('utf-8'))
    # Return the hexadecimal representation of the hash
    return sha256.finalize().hex()


def base64_encode(input_dict):
    # Convert the dictionary to a JSON string
    json_data = jsons.dumps(input_dict)
    # Encode the JSON string to bytes
    data_bytes = json_data.encode('utf-8')
    # Perform Base64 encoding and return the result as a string
    return base64.b64encode(data_bytes).decode('utf-8')

def generate_secure_token(data):
    signer = signing.Signer()
    return signer.sign(data)

def verify_secure_token(token):
    signer = signing.Signer()
    try:
        return signer.unsign(token)
    except signing.BadSignature:
        return None


def pay(request):
    booking_ids = request.POST.getlist('booking_ids')
    booking_ids_str = ','.join(booking_ids)
    encrypted_booking_ids = signing.dumps(booking_ids_str)

    MAINPAYLOAD = {
        "merchantId": "PGTESTPAYUAT86",
        "merchantTransactionId": shortuuid.uuid(),
        "merchantUserId": "MUID123",
        "amount": 100,  # query up the amount for the bookings data-base
        "redirectUrl": f"http://127.0.0.1:8000/payment/paymentreturn/?token={encrypted_booking_ids}",
        "redirectMode": "POST",
        "callbackUrl": f"http://127.0.0.1:8000/payment/paymentreturn/?token={encrypted_booking_ids}",
        "mobileNumber": "9999999999",
        "paymentInstrument": {
            "type": "PAY_PAGE"
        }
    }

    INDEX = "1"
    ENDPOINT = "/pg/v1/pay"
    SALTKEY = "96434309-7796-489d-8924-ab56988a6076"

    base64String = base64_encode(MAINPAYLOAD)
    mainString = base64String + ENDPOINT + SALTKEY
    sha256Val = calculate_sha256_string(mainString)
    checkSum = sha256Val + '###' + INDEX

    headers = {
        'Content-Type': 'application/json',
        'X-VERIFY': checkSum,
        'accept': 'application/json',
    }
    json_data = {
        'request': base64String,
    }
    response = requests.post('https://api-preprod.phonepe.com/apis/pg-sandbox/pg/v1/pay', headers=headers, json=json_data)
    responseData = response.json()
    print(responseData)
    return redirect(responseData['data']['instrumentResponse']['redirectInfo']['url'])


@csrf_exempt
def payment_return(request):
    token = request.GET.get('token')
    try:
        booking_ids_str = signing.loads(token)
        booking_ids = booking_ids_str.split(',')
    except signing.BadSignature:
        return HttpResponse("Invalid token", status=400)

    INDEX = "1"
    SALTKEY = "96434309-7796-489d-8924-ab56988a6076"

    form_data = request.POST
    form_data_dict = dict(form_data)

    transaction_id = form_data.get('transactionId', None)

    if transaction_id:
        request_url = f'https://api-preprod.phonepe.com/apis/pg-sandbox/pg/v1/status/PGTESTPAYUAT86/{transaction_id}'
        sha256_Pay_load_String = f'/pg/v1/status/PGTESTPAYUAT86/{transaction_id}{SALTKEY}'
        sha256_val = calculate_sha256_string(sha256_Pay_load_String)
        checksum = sha256_val + '###' + INDEX

        headers = {
            'Content-Type': 'application/json',
            'X-VERIFY': checksum,
            'X-MERCHANT-ID': transaction_id,
            'accept': 'application/json',
        }
        response = requests.get(request_url, headers=headers)
        response_data = response.json()

        bookings = Booking.objects.filter(id__in=booking_ids)

        for booking in bookings:
            booking.booking_status = True
            if response.status_code == 200 and response_data.get('code') == "PAYMENT_SUCCESS" and response_data['data'].get('state') == "COMPLETED":
                booking.payment_status = True
            booking.save()

        if response.status_code == 200 and response_data.get('code') == "PAYMENT_SUCCESS" and response_data['data'].get('state') == "COMPLETED":
            send_confirmation_mail_vendor_professionals(bookings)
            send_confirmation_mail_user(bookings)
        
        return render(request, 'Payment/checkout.html', {'output': response.text, 'main_request': form_data_dict})
    else:
        return HttpResponse("Transaction ID not found", status=400)


def send_confirmation_mail_user(bookings):
    
    user_email = bookings[0].user.email  

    # Prepare email subject and content
    subject = 'Booking Confirmation and Payment Success'
    context = {
        'bookings': bookings,
        'total_amount': sum(booking.total_price for booking in bookings),
        'success_message': 'Your payment is successful.',
    }

    html_message = render_to_string('Payment/confirmation_email.html', context)

    # Send email using send_mail function
    send_mail(
        subject,
        '',
        settings.EMAIL_HOST_USER,  
        [user_email],
        html_message=html_message,
        fail_silently=True
    )


def send_confirmation_mail_vendor_professionals(bookings):
    for booking in bookings:
        if booking.venue:  
            # Send email to vendor
            vendor_email = booking.venue.contact_email 
            subject = 'New Booking Confirmation'
            context = {
                'booking': booking,
                'success_message': 'A new booking has been made for your venue.',
            }
            html_message = render_to_string('Payment/vendor_confirmation_email.html', context)
            send_mail(
                subject,
                '',  
                settings.EMAIL_HOST_USER,  
                [vendor_email],
                html_message=html_message,
            )
        elif booking.professional:  
            # Send email to professional
            professional_email = booking.professional.contact_email 
            subject = 'New Booking Confirmation'
            context = {
                'booking': booking,
                'success_message': 'A new booking has been made for your professional services.',
            }
            html_message = render_to_string('Payment/professional_confirmation_email.html', context)
            send_mail(
                subject,
                '',  
                settings.EMAIL_HOST_USER, 
                [professional_email],
                html_message=html_message,
            )
