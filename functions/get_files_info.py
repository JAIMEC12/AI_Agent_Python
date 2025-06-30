import os
from google.genai import types

def get_files_info(working_directory, directory=None):

    path = os.path.abspath(working_directory)

    if directory:
        path = os.path.join(os.path.abspath(working_directory),directory)

    # if directory.startswith(".") and "../" not in directory:
    #     directory= working_directory
    #     path = directory
    
    if not os.path.abspath(path).startswith(os.path.abspath(working_directory)):
        return f"Error: Cannot list '{directory}' as it is outside the permitted working directory"
    
    if not os.path.isdir(path):
        return f"Error: '{directory}' is not a directory"
    
    content_info = get_content(path)
    
    return content_info


def get_content(directory_content):
    list_content = []
    try:
        for content in os.listdir(directory_content):
            content_info=f"- {content}: file_size={os.path.getsize(os.path.join(directory_content,content))}, is_dir={os.path.isdir(os.path.join(directory_content,content))}"
            list_content.append(content_info)
        content_result = "\n".join(list_content)
        return content_result
    except Exception as e:
        return f"Error: {e}"


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory. ",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself. That means '.' "
                ),
            },
        ),
    )