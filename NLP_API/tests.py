from django.test import TestCase
from rest_framework.test import APIClient
from unittest.mock import patch
import json


class SentimentAnalysisViewTestCase(TestCase):

    @patch("NLP_API.views.analyze_sentiment")
    def test_sentiment_analysis(self, mock_analyze_sentiment):
        client = APIClient()

        mock_analyze_sentiment.side_effect = (
            lambda text: f"Sentiment analysis result for '{text}'"
        )

        # Test case 1
        data = {"user_input": ["good on you"]}
        response = client.post(
            "/api/sentiment-analysis/",
            data=json.dumps(data),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(
            response.data["results"][0], "Sentiment analysis result for 'good on you'"
        )

        # Test case 2: Multiple inputs sentiment analysis
        data = {"user_input": ["good on you", "get in there"]}
        response = client.post(
            "/api/sentiment-analysis/",
            data=json.dumps(data),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(
            response.data["results"][0], "Sentiment analysis result for 'good on you'"
        )
        self.assertEqual(
            response.data["results"][1], "Sentiment analysis result for 'get in there'"
        )
