from django.http import HttpRequest

def get_client_ip(request:HttpRequest):
    http_forward=request.META.get('Http_X_FORWARDED_FOR')

    if http_forward:
        ip=http_forward.split(',')[0]
    else:
        ip=request.META.get('REMOTE_ADDR')
    
    return ip