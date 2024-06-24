from transformers import pipeline
import asyncio
from concurrent.futures import ThreadPoolExecutor


classifier = pipeline(
    "sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english"
)


async def analyze_sentiment(text):
    with ThreadPoolExecutor() as executor:
        result = await asyncio.get_event_loop().run_in_executor(
            executor, classifier, text
        )
    return result
