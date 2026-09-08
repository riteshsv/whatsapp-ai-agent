import os
from langchain.rate_limiters import InMemoryRateLimiter
from langchain_google_genai import ChatGoogleGenerativeAI
sales_agent_api = "AIzaSyCCG509WB1KOFgPPbs4_i6d6adc9UNnEHM"
gemini_free_key = "AIzaSyAfdjKsWNZLPTfFNHRQ79IE2oAN-Dc3Omo"
os.environ["GOOGLE_API_KEY"] = sales_agent_api

rate_limiter = InMemoryRateLimiter(
    requests_per_second= 4 / 60,
    check_every_n_seconds=0.1,
    max_bucket_size=1,
)

model = ChatGoogleGenerativeAI(model="gemini-3.7-flash",
                               temperature=0,
                               rate_limiter=rate_limiter)