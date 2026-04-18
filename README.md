# Weather AI Agent

This repository contains a small reactive weather assistant built around a language model and a hardcoded weather lookup function.

## Overview

The project demonstrates two weather agent variants that ask a model whether the user should take an umbrella, then consult a weather function before answering:

- `weather_agent.py` - a reactive loop that sends model prompts, extracts JSON actions, calls `get_weather`, and continues until an answer is found.
- `weather_agent_simpler.py` - a simplified reactive agent using `SimplerLLM` and JSON extraction.
- `embed_agent.py` - a minimal hardcoded example that calls `generate_response` directly with current weather data.

## Files

### `weather_info.py`
Contains a placeholder function `get_weather_by_city(city)` that returns hardcoded weather states for a few cities.

### `weather_agent.py`
- Imports a Gemini response wrapper from `gemini_connect`.
- Uses `react_prompts.react_system_prompt` to define the Thought/Action/PAUSE/Action_Response agent flow.
- Uses `json_util.extract_json` to parse model-selected function calls.
- Dispatches a `get_weather` action and feeds the result back to the model.

### `weather_agent_simpler.py`
- Loads environment variables with `dotenv`.
- Uses `SimplerLLM` and `LLMProvider.GEMINI` for model interaction.
- Uses `SimplerLLM.tools.json_helpers.extract_json_from_text` to parse function calls.
- Runs a loop, executes the weather action, and appends the response.

### `react_prompts.py`
Defines the system prompt guiding the model to:
- think in `Thought`
- select an action in `Action`
- pause with `PAUSE`
- receive the tool result in `Action_Response`
- output a final `Answer`

### `json_util.py`
Provides a helper to extract JSON objects from a text response using regex and bracket nesting.

### `google_models_list.py`
Connects to Google Gemini and prints available models whose names contain `gemma`.

### `embed_agent.py`
A hardcoded example that looks up Ottawa weather, sends a prompt to `generate_response`, and prints the model answer.

## Usage

1. Activate the virtual environment:

```powershell
.\myenv\Scripts\Activate.ps1
```

2. Install required dependencies for the files used in this repository.
   Based on imports, the project likely needs:
   - `python-dotenv`
   - `SimplerLLM`
   - Gemini/Google client libraries used by `gemini_connect`

3. Run one of the agent scripts:

```powershell
python .\weather_agent.py
```

or

```powershell
python .\weather_agent_simpler.py
```

or

```powershell
python .\embed_agent.py
```

## Notes

- `weather_info.py` currently uses hardcoded weather values, so the agent is a demonstration of reactive prompting rather than a production weather service.
- `weather_agent_simpler.py` expects `.env` configuration for the Gemini provider.
- `google_models_list.py` is useful for discovering available Gemini models.
