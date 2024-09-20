from django.shortcuts import render

#below function loads the landingpage html

def landing_view(request):
    image_list = [
        '..\\media\\venue_images\\Ahluwalia_PLC_60.jpg',
        '..\\media\\venue_images\\Arora-Gandhi_22.jpg',
        '..\\media\\venue_images\\Bal_Baral_and_Majumdar_17.jpg',
    ]
    return render(request, 'Mainpage/landingpage.html', {'images': image_list})

