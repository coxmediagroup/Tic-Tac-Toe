import json

def json_response(status, msg):
    from django.http import HttpResponse
    response = {"status": status, "msg": msg}
    return HttpResponse(json.dumps(response))

