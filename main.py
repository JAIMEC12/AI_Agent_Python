import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")


def main():
    client = genai.Client(api_key=api_key)
    verbose = True if "--verbose" in sys.argv else False
    args_no_flags = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if len(sys.argv)> 1:
        user_prompt = " ".join(args_no_flags)
        print(f"User prompt: {user_prompt}")
        messages = [
            types.Content(role="user",parts=[types.Part(text=user_prompt)])
        ]
        generate_content(client,messages,verbose)
    else:
        print("Error, there is no prompt. In order to use this AI Code Assistant you need to execute main.py with an argument next to it")
        print("Example: python main.py 'What is Python'")
        sys.exit(1)


def generate_content(client,messages,verbose):
    response = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages)
    if verbose:
      print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\n")
      print(f"Response tokens: {response.usage_metadata.candidates_token_count}\n")
    print(f"Response: {response.text}")


if __name__ == "__main__":
    main()