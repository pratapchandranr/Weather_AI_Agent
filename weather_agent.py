#Reactive Agent calling functions
from urllib import response
from xml.parsers.expat import model

from gemini_connect import generate_response
from weather_info import get_weather_by_city
from react_prompts import react_system_prompt
from json_util import extract_json
from gemini_connect import generate_response_with_functions

#Weather Action
weather_action = {
    "get_weather": get_weather_by_city
}

prompt = f"""Should I take an umbrella when going outside today in Montreal?"""

messages = [
    {"role": "system", "content": react_system_prompt},
    {"role": "user", "content": prompt},
]

#In a real implementation, you would parse the response to check for Thought, Action, PAUSE, and Action_Response.
#For simplicity, we will just print the response here.  
print(f'Model Response: {response}')

turn_count = 1
max_turns = 5

while turn_count <= max_turns:
    print(f"==================== Turn {turn_count} ====================")
    print(f"Turn {turn_count} - Sending messages to model...")
    
    response = generate_response_with_functions(messages, model="gemma-3-27b-it")
    print(f"Model Response: {response}\n")

    # Add assistant response to messages
    messages.append({"role": "user", "content": response})
    
    # Check if the answer is found (stop condition)
    if "Answer:" in response:
        print(f"\nFinal Answer found at Turn {turn_count}")
        break
    
    # Extract JSON from response
    json_response = extract_json(response)
    print(f"Extracted JSON: {json_response}")
    
    if json_response and isinstance(json_response, list) and len(json_response) > 0:
        json_data = json_response[0]  # Get the first dictionary from the list
        function_name = json_data.get("function_name")
        function_parms = json_data.get("function_parms")
        
        if function_name and function_parms and function_name in weather_action:
            print(f"Calling function: <function {weather_action[function_name].__name__}> with parameters: {function_parms}")
            action_result = weather_action[function_name](**function_parms)
            print(f"Action Result: {action_result}\n")
            # Add action response to messages for next turn
            messages.append({"role": "user", "content": f"Action_Response: {action_result}"})
        else:
            print(f"Function {function_name} not found in available actions.")
            break
    else:
        print("No valid JSON found in response")
        break
    
    turn_count += 1


