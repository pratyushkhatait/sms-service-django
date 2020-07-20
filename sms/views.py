import datetime
import logging
from rest_framework.views import APIView
from rest_framework.serializers import ValidationError
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponse
from sms.serializers import InboundSerializer, OutboundSerializer
from sms.utilities.redis_utils import redis
from sms.config import CACHE_TTL
logger = logging.getLogger(__name__)


class Ping(APIView):
    """
    This Ping API is  used to test the working of Django API
    """
    http_method_names = ['get']

    def get(self):
        return HttpResponse("Pong")


class InboundSMSView(APIView):
    serializer_class = InboundSerializer
    http_method_names = ['post']

    def post(self, request):
        """
        This Post API executes inbound SMS from an account's phone number to others
        :param request:
        :return:
        """
        logger.info("InboundSMSView: starts execution")
        inbound_serializer = self.serializer_class(data=request.data)
        try:
            inbound_serializer.is_valid(raise_exception=True)
        except ValidationError as err:
            logger.error("InboundSMSView: Error occurred: error::{}".format(str(err)))
            resp = {
                'message': "",
                'error': ""
            }
            for param, err_msg in err.get_codes().items():
                if err_msg[0] == "required":
                    resp["error"] += "{} is missing".format(param) if not resp["error"] else ", {} is missing".format(param)
                elif err_msg[0] == "min_length" or err_msg[0] == "max_length":
                    resp["error"] = "{} is invalid".format(param)
                elif err_msg[0] == "invalid":
                    resp["error"] = "to parameter not found"
                else:
                    resp["error"] = "unknown failure"

            status_code = status.HTTP_400_BAD_REQUEST
            return Response(resp, status=status_code)

        validated_data = inbound_serializer.validated_data

        # When text is STOP or STOP\n or STOP\r or STOP\r\n  Cache the ‘from’ and ‘to’ pair for 4 hours
        if validated_data["_text"].startswith("STOP"):
            redis_key = "sms:{}:{}".format(validated_data["_from"], validated_data["_to"])
            redis.set_redis_object(redis_key, 1, expiry=CACHE_TTL)
            logger.info("InboundSMSView: Successfully cached the 'from' and 'to' pair for 4 hours")

        resp = {
            "message": "inbound sms ok",
            "error": ""
        }
        logger.info("InboundSMSView: Successfully executed inbound sms")
        return Response(resp, status=status.HTTP_200_OK)


class OutboundSMSView(APIView):
    serializer_class = OutboundSerializer
    http_method_names = ['post']

    def post(self, request):
        """
        This Post API executes outbound SMS from an account's phone number to others
        :param request:
        :return:
        """
        logger.info("OutboundSMSView: starts execution")
        outbound_serializer = self.serializer_class(data=request.data)
        try:
            outbound_serializer.is_valid(raise_exception=True)
        except ValidationError as err:
            logger.error("OutboundSMSView: Error occurred: error::{}".format(str(err)))
            resp = {
                'message': "",
                'error': ""
            }
            for param, err_msg in err.get_codes().items():
                if err_msg[0] == "required":
                    resp["error"] += "{} is missing".format(param) if not resp["error"] else ", {} is missing".format(param)
                elif err_msg[0] == "min_length" or err_msg[0] == "max_length":
                    resp["error"] = "{} is invalid".format(param)
                elif err_msg[0] == "invalid":
                    resp["error"] = "from parameter not found"
                else:
                    resp["error"] = "unknown failure"

            status_code = status.HTTP_400_BAD_REQUEST
            return Response(resp, status=status_code)
        validated_data = outbound_serializer.validated_data

        # Do not allow more than 50 API requests using the same ‘from’ number in 24 hours
        count_key = "outbound:{}:{}".format(validated_data["_from"], str(datetime.datetime.now().date()))
        current_API_hits = redis.get_redis_object(count_key)
        if current_API_hits and current_API_hits >= 50:
            resp = {
                "message": "",
                "error": "limit reached for {}".format(validated_data["_from"])
            }
            return Response(resp, status=status.HTTP_200_OK)

        # If the total number of API requests is less than 50, then increment the api_hit_count
        redis.increment_redis_object(count_key)

        # Check cache if the 'from' is blocked by STOP request
        redis_key = "sms:{}:{}".format(validated_data["_from"], validated_data["_to"])
        redis_data = redis.get_redis_object(redis_key)
        if redis_data:
            resp = {
                "message": "inbound sms ok",
                "error": "sms from {} to {} blocked by STOP request".format(validated_data["_from"], validated_data["_to"])
            }
            logger.error("OutboundSMSView: sms from {} to {} blocked by Stop request".format(
                validated_data['_from'], validated_data['_to']))
            return Response(resp, status=status.HTTP_200_OK)
        resp = {
            "message": "outbound sms ok",
            "error": ""
        }
        logger.info("outboundSMSView: Successfully executed inbound sms")
        return Response(resp, status=status.HTTP_200_OK)
