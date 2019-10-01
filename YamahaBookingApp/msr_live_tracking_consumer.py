from channels import Group
from channels.handler import AsgiHandler, AsgiRequest
from django.http import HttpResponse
from django.utils.timezone import now
from json import dumps
from .models import *

from datetime import datetime

# def http_consumer(message):
#     # Make standard HTTP response - access ASGI path attribute directly
#     response = HttpResponse("Hello world! You asked for %s" % message.content['path'])
#     # Encode that response into message format (ASGI)
#     for chunk in AsgiHandler.encode_response(response):
#         message.reply_channel.send(chunk)

def http_consumer(message):
    response = HttpResponse(
        "It is now {} and you've requested {} with {} as request parameters.".format(
            now(),
            message.content['path'],
            dumps(message.content['get'])
        )
    )
    message.reply_channel.send(response.channel_encode())


def ws_message(message):
    # ASGI WebSocket packet-received and send-packet message types
    # both have a "text" key for their textual data.
    #print("Incoming text from Socket: " + str(message.content))
    #msr_initial_locations = GetInitialMSRPosition()
    print('--message--'+str(message.content['text']))

    data = "OK"
    # for msr in msr_initial_locations:
    #     data += str(msr['ID']) + '|' + str(msr['UserId']) + '|' + str(msr['Level1Name']) + '|' + str(msr['Latitude'])+ '|' + str(msr['Longitude']) + '|' + str(msr['MaxUpdateTime'])
    #     data += '||'
    #print(data)
    message.reply_channel.send({
        "text": data
    })

def ws_connect(message):
    # Group('users').add(message.reply_channel)
    print('Test1' + message)


def ws_disconnect(message):
    # Group('users').discard(message.reply_channel)
    print('Test2' + message)

    message.discard(message.reply_channel)


def my_consumer(message):
    print(('yesdss' + message.handle))
    # response = HttpResponse("Hello world! You asked for %s" % message.content['path'])
    django_request = AsgiRequest(message)
    # Run view
    response = HttpResponse("Hello world! You asked for %s" % message.content['path'])
    # Encode that response into message format (ASGI)
    for chunk in AsgiHandler.encode_response(response):
        message.reply_channel.send(chunk)



# def ws_disconnect(message):
#     label = message.channel_session['room']
#     Group('chat-'+label).discard(message.reply_channel)
