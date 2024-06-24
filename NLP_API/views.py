from adrf.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from .serializers import SentimentSerializer
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers
from .utils import analyze_sentiment
import logging
import time

logger = logging.getLogger("api_logger")


class AsyncNLPView(APIView):
    @extend_schema(
        request=inline_serializer(
            name="SentimentSerializer",
            fields={"user_input": serializers.ListField(child=serializers.CharField())},
        )
    )
    async def post(self, request):
        try:
            from_cache = False
            start_time = time.time()

            serialized_data = SentimentSerializer(data=request.data)
            serialized_data.is_valid(raise_exception=True)
            results = []

            inputs = serialized_data.validated_data["user_input"]
            cache_key = hash(tuple(inputs))
            cached_result = cache.get(cache_key)
            if cached_result:

                duration = time.time() - start_time
                logger.info(f"Success with duration of {duration},CACHE HIT")
                return Response(cached_result, status=status.HTTP_200_OK)

            results = [await analyze_sentiment(input) for input in inputs]
            # for input, result in zip(inputs, results):
            #     result_dict = {}
            #     result_dict[input] = result
            #     result.append(result_dict)
            duration = time.time() - start_time
            logger.info(f"Success with duration of {duration},CACHE MISS")
            return Response({"results": results})
        except Exception as e:
            logger.error(f"Error: Error type {str(e)}")
            return Response({"result": "Something went wrong"})
