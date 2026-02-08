import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from prompts import system_prompt

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
    
token_count = genai.types.GenerateContentResponse
print (token_count)

client = genai.Client(api_key=api_key)
response = client.models.generate_content(
    model='gemini-2.5-flash', 
    contents= messages,
    config= types.GenerateContentConfig(
        system_instruction = system_prompt,
        max_output_tokens = 3000,
        temperature = 0
        ) 
)
if response.usage_metadata == None:
    raise RuntimeError ("metadata not available")


response_tokens = response.usage_metadata.candidates_token_count
prompt_tokens = response.usage_metadata.prompt_token_count


if args.verbose == True:
    print(f"User prompt: {messages}")
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {response_tokens}")
    print("Response:")
    print(response.text)
else:
    print(response.text)





def main():
    


    if __name__ == "__main__":
        main()