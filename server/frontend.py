from django.http import HttpResponse
from chatbot import bot1, bot2


def chatbot_1(request):
    return chatbot_request(request, bot1())


def chatbot_2(request):
    return chatbot_request(request, bot2())


def chatbot_request(request, bot):
    data = request.GET.get("data")
    if data:
        response = bot.response(data)
        return HttpResponse(response, mimetype='application/text')
    else:
        return HttpResponse('Please enter some text', mimetype='application/text')
