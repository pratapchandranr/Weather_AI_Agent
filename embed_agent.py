#Hardcoded Agent
from xml.parsers.expat import model

from gemini_connect import generate_response
from weather_info import get_weather_by_city

current_weather = get_weather_by_city("Ottawa")

prompt = f"The current weather in Ottawa is {current_weather}. Should I take an umbrella when going outside today?"
response = generate_response(prompt, model="gemma-3-27b-it")

print(response)


