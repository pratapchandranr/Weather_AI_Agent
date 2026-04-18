#Reactive Agent calling functions
from dotenv import load_dotenv
from react_prompts import react_system_prompt
from weather_info import get_weather_by_city
from SimplerLLM.language.llm import LLM, LLMProvider
from SimplerLLM.tools.json_helpers import extract_json_from_text

# Load environment variables from .env file
load_dotenv()

llm_instance = LLM.create(provider=LLMProvider.GEMINI,model_name="gemini-flash-latest")

weather_action = {
    "get_weather": get_weather_by_city
}

prompt = f"""What is the weather like in Delhi today?"""

messages = [
    {"role": "system", "content": react_system_prompt},
    {"role": "user", "content": prompt},
]

#In a real implementation, you would parse the response to check for Thought, Action, PAUSE, and Action_Response.
#For simplicity, we will just print the response here.  
#print(f'Model Response: {response}')

turn_count = 1
max_turns = 5

while turn_count < max_turns:
    print (f"Loop: {turn_count}")
    print("----------------------")
    turn_count += 1

    response = llm_instance.generate_response(messages=messages)

    print(response)

    json_function = extract_json_from_text(response)

    if json_function:
            function_name = json_function[0]['function_name']
            function_parms = json_function[0]['function_parms']
            if function_name not in weather_action:
                raise Exception(f"Unknown action: {function_name}: {function_parms}")
            print(f" -- running {function_name} {function_parms}")
            action_function = weather_action[function_name]
            #call the function
            result = action_function(**function_parms)
            function_result_message = f"Action_Response: {result}"
            messages.append({"role": "user", "content": function_result_message})
            print(function_result_message)
    else:
         break