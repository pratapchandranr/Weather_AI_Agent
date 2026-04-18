from gemini_connect import connect_to_google

with connect_to_google() as client:
    for model in client.models.list():
        if 'gemma' in model.name:
            print(model.name)