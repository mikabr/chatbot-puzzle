from django.http import HttpResponse
from chatbot import bot1, bot2
#from chatbot import bot


#def chatbot(request):
#    return chatbot_request(request, bot())

def chatbot_1(request):
    return chatbot_request(request, bot1())

def chatbot_2(request):
    return chatbot_request(request, bot2())

#def chatbot_reset(request):
#    session_key = 'chatbot'
#    request.session[session_key] = 0
#    return HttpResponse('reset', mimetype='application/text')

def chatbot_request(request, bot):
    data = request.GET.get("data")
#    session_key = 'chatbot'
    if data:
#        if session_key not in request.session:
#            request.session[session_key] = 0
#        character = request.session[session_key]
#        response = bot.response(data, character)
        response = bot.response(data)
#        request.session[session_key] = character + 1
        return HttpResponse(response, mimetype='application/text')
    else:
        return HttpResponse('Please enter some text', mimetype='application/text')
