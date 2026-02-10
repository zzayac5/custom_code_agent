import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from prompts import system_prompt
from call_function import available_functions

#User input using argparse#

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
# Now we can access `args.user_prompt`

#building the messages#
messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]


#load gemini api#

load_dotenv()
 
api_key = os.environ.get("GEMINI_API_KEY")
if api_key == None:
    raise RuntimeError("api keys are missing")  
    
client = genai.Client(api_key=api_key)
response = client.models.generate_content(
    model='gemini-2.5-flash', 
    contents= messages,
    config= types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction = system_prompt,
        max_output_tokens = 3000,
        temperature = 0,
        ) 
)
if response.usage_metadata == None:
    raise RuntimeError ("metadata not available")


response_tokens = response.usage_metadata.candidates_token_count
prompt_tokens = response.usage_metadata.prompt_token_count


if response.function_calls:
    # Optionally some verbose info *before* the calls:
    if args.verbose:
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")

    for function_call in response.function_calls:
        print(f"Calling function: {function_call.name}({function_call.args})")
else:
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")
        print("Response:")

    print(response.text)

def main():
    

    if __name__ == "__main__":
        main()