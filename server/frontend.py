from django.http import HttpResponse
from chatbot import bot1, bot2


def chatbox_1(request, data):
    response = bot1().response(data)
    return HttpResponse(response, mimetype='application/text')


def chatbox_2(request, data):
    response = bot2().response(data)
    return HttpResponse(response, mimetype='application/text')
