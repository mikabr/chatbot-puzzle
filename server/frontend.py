from django.http import HttpResponse
from chatbot import bot1, bot2


def chatbot_1(request):
    response = bot1().response(request.POST.get("data"))
    return HttpResponse(response, mimetype='application/text')


def chatbot_2(request):
    response = bot2().response(data)
    return HttpResponse(response, mimetype='application/text')
