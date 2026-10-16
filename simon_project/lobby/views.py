from django.shortcuts import render

def index(request):
    return render(request, "base.html")

def test_websocket(request):
    return render(request, "lobby/test_websocket.html")

def preview_error(request, code):
    if code not in (400, 403, 404, 500):
        raise Http404
    return render(request, f"{code}.html", status=code)