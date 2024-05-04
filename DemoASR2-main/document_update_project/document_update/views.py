import requests
from django.shortcuts import render
from django.http import HttpResponse
from .models import Usuario
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail

URLS = [
    "https://basedatostarjeta.000webhostapp.com/request.php",
    "https://activos000.000webhostapp.com/request.php",
    "https://alpestarjeta.000webhostapp.com/request.php"
]

@csrf_exempt
def upload_file(request):
    user_name = None
    user_estado = None
    error_message = None
    usuarios = Usuario.objects.all()
    check_urls()
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        if user_id:
            server_available = False
            for url in URLS:
                try:
                    response = requests.get(url, params={'id': user_id})
                    if response.status_code == 200:
                        data = response.json()
                        if 'error' in data:
                            error_message = data['error']
                        else:
                            user_name = data['nombre']
                            user_estado = data['estado']
                            server_available = True
                        break
                except requests.ConnectionError as e:
                    print("Connection error:", str(e))
                    continue

            if not server_available:
                error_message = 'Lamentablemente, no podemos completar su solicitud. Si así lo desea, podemos enviarle un correo electrónico en cuanto este servicio esté disponible nuevamente.'
                return render(request, 'upload_file.html', {'user_name': user_name, 'user_estado': user_estado, 'error_message': error_message, 'usuarios': usuarios, 'email_required': True})
                
            return render(request, 'upload_file.html', {'user_name': user_name, 'user_estado': user_estado, 'error_message': error_message, 'usuarios': usuarios})

        else:
            error_message = 'ID de usuario no proporcionado.'

    return render(request, 'upload_file.html', {'error_message': error_message, 'usuarios': usuarios})

@csrf_exempt
def process_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            try:
                with open('./document_update/emails.txt', 'a') as file:
                    file.write(email + '\n')
                    print("Email written to file:", email)
            except Exception as e:
                print("Error writing email to file:", str(e))
            
            error_message = "Correo electrónico registrado con éxito"
            usuarios = Usuario.objects.all() 

            return render(request, 'upload_file.html', {'error_message': error_message, 'usuarios': usuarios})

def send_email():
    subject = 'Solicitud de tarjeta'
    message = 'Los servicios de comprobación del estado de su solicitud están nuevamente disponibles.'
    email_from = 'a.serranoc@uniandes.edu.co'
    recipient_list = []
    with open('./document_update/emails.txt', 'r') as file:
        for line in file:
            recipient_list.append(line.strip())

    with open('./document_update/emails.txt', 'w') as file:
        file.write('')

    send_mail(subject, message, email_from, recipient_list)
def check_urls():
    for url in URLS:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                send_email()
                print(f"Server {url} is up")
                return True  
        except requests.ConnectionError as e:
            print(f"Connection error to {url}: {str(e)}")
            continue
    
    print("No server is available")
    return False

