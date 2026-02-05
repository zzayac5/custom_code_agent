import os
from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()
 
api_key = os.environ.get("GEMINI_API_KEY")
if api_key == None:
    raise RuntimeError("api keys are missing")  
    
token_count = genai.types.GenerateContentResponse
print (token_count)

client = genai.Client(api_key=api_key)
response = client.models.generate_content(
    model='gemini-2.5-flash', 
    contents='"Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."',
    MetaData = types.GenerateContentResponseUsageMetadata(
        prompt_token_count= int,
        candidates_token_count= int
    )
)


print(f"Prompt tokens: {client}")

print(response.text)

def main():
    


    if __name__ == "__main__":
        main()