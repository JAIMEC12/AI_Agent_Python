import os
from google.genai import types

def get_file_content(working_directory, file_path):
    path = os.path.join(os.path.abspath(working_directory),file_path)
    
    if not os.path.abspath(path).startswith(os.path.abspath(working_directory)):
        return f"Error: Cannot read '{file_path}' as it is outside the permitted working directory"

    if not os.path.isfile(path):
        return f"Error: File not found or is not a regular file: '{file_path}'"
    
    return read_file(path)


def read_file(file):
    MAX_CHARS = 10000
    try:
        with open(file,"r", encoding="utf-8") as f:
            string_text = f.read(MAX_CHARS)
            return string_text if len(string_text)<MAX_CHARS else string_text + f"...File '{file}' truncated at 10000 characters"
    except Exception as e:
        return f"Error: {e}"
    

    
schema_get_files_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read the content from the specified file constrained to the working directory. If the file has more than 10000 characters, it truncates at 10000.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path where the file to get its content is located, relative to the working directory."
                ),
            },
        ),
    )
