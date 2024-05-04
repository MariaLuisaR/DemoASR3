from django.shortcuts import render
from django.http import JsonResponse
import requests

def check_link_status(link):
    try:
        response = requests.get(link)
        return response.status_code == 200
    except requests.ConnectionError:
        return False

def server_list(request):
    links = [
        "https://basedatostarjeta.000webhostapp.com/request.php",
        "https://activos000.000webhostapp.com/request.php",
        "https://alpestarjeta.000webhostapp.com/request.php"
    ]

    servers = []
    for link in links:
        status = "Active" if check_link_status(link) else "Inactive"
        servers.append({
            "name": link,
            "status": status
        })

    return render(request, 'monitoring/server_list.html', {'servers': servers})

def check_links(request):
    links = [
        "https://basedatostarjeta.000webhostapp.com/request.php1",
        "https://activos000.000webhostapp.com/request.php1",
        "https://alpestarjeta.000webhostapp.com/request.php1"
    ]

    statuses = {}
    for link in links:
        status = "Active" if check_link_status(link) else "Inactive"
        statuses[link] = status

    return JsonResponse(statuses)
