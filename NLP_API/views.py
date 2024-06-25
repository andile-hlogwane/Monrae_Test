from adrf.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from .serializers import SentimentSerializer
from rest_framework.exceptions import ParseError
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers
from .utils import analyze_sentiment
import logging
import time

logger = logging.getLogger("api_logger")


class AsyncNLPView(APIView):
    """async class view for sentiment analysis"""

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
            cached_result = {"results": results}
            cache.set(cache_key, cached_result)
            duration = time.time() - start_time
            logger.info(f"Success with duration of {duration},CACHE MISS")
            return Response({"results": results}, status=status.HTTP_200_OK)
            
        except serializers.ValidationError as e:
            logger.error(f"Validation error: {str(e)}")
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

        except ParseError as e:
            logger.error(f"JSON parse error: {str(e)}")
            return Response(
                {"result": f"JSON parse error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            logger.error(f"Error: Error type {str(e)}")
            return Response(
                {"result": "Something went wrong"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

