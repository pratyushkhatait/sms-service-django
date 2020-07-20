from django.conf.urls import url
from sms.views import (InboundSMSView, OutboundSMSView, Ping)

urlpatterns = [
    # Ping Pong API
    url(r'^ping/$', Ping.as_view(), name='ping'),
    # Inbound SMS
    url(r'^inbound/sms/$', InboundSMSView.as_view(), name='inbound'),
    # Outbound SMS
    url(r'^outbound/sms/$', OutboundSMSView.as_view(), name='outbound'),
]
