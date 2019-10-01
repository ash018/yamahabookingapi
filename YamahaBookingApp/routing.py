# from channels.routing import route
#
#
# # channel_routing = [
# #     route('websocket.connect', ws_connect),
# #     route('websocket.disconnect', ws_disconnect),
# # ]route("websocket.receive", ws_message),
# twitter_channel_routing = {
#     "some-channel": "YamahaBookingApp.msr_live_tracking_consumer.my_consumer",
#     #"http.request": "aianalytics.consumers.http_consumer",
#     "websocket.receive": "YamahaBookingApp.msr_live_tracking_consumer.ws_message",
#     #"websocket.disconnect": "aianalytics.consumers.ws_disconnect",
# }