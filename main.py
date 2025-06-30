import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_file_content import schema_get_files_content, get_file_content
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.write_file import schema_write_file, write_file
from functions.run_python_file import schema_run_python_file, run_python_file
import sys

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")


def main():
    client = genai.Client(api_key=api_key)
    verbose = True if "--verbose" in sys.argv else False
    args_no_flags = [arg for arg in sys.argv[1:] if not arg.startswith("--")]
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite file

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

    if len(sys.argv)> 1:
        user_prompt = " ".join(args_no_flags)
        print(f"User prompt: {user_prompt}")
        messages = [
            types.Content(role="user",parts=[types.Part(text=user_prompt)])
        ]
        generate_content(client,messages,verbose,system_prompt)
    else:
        print("Error, there is no prompt. In order to use this AI Code Assistant you need to execute main.py with an argument next to it")
        print("Example: python main.py 'What is Python'")
        sys.exit(1)


def generate_content(client,messages,verbose, system_prompt):

    available_functions = types.Tool(
        function_declarations=[schema_get_files_info,schema_get_files_content,schema_run_python_file,schema_write_file]
    )

    config= types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)

    response = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages,config=config)
    

    if verbose:
      print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\n")
      print(f"Response tokens: {response.usage_metadata.candidates_token_count}\n")

    function_response = []
    
    if response.function_calls:
        for function in response.function_calls:
            function_call_result = call_function(function, verbose)
            if not function_call_result.parts or not function_call_result.parts[0].function_response:
                raise Exception("empty function results")
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            function_response.append(function_call_result.parts[0])
    
        if not function_response:
            raise Exception("No response from functions")
    else:
        return response.text


def call_function(function_call_part, verbose = False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    
    functions_name = {
        "get_files_info" : get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }

    if function_call_part.name not in functions_name:
        return types.Content(
            role = "tools",
            parts = [
                types.Part.from_function_response(
                    name = function_call_part.name,
                    response = {"error": f"Unkwon function: {function_call_part.name}"},
                )
            ],
        )
    args = dict(function_call_part.args)
    args["working_directory"] = "./calculator"
    return types.Content(
        role = "tools",
        parts=[
            types.Part.from_function_response(
                name= function_call_part.name,
                response = {"result": functions_name[function_call_part.name](**args)},
            )
        ],
    )


if __name__ == "__main__":
    main()