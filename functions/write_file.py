import os
from google.genai import types

def write_file(working_directory, file_path, content):
   
   path = os.path.join(working_directory,file_path)

   if not os.path.abspath(path).startswith(os.path.abspath(working_directory)):
        return f"Error: Cannot write '{file_path}' as it is outside the permitted working directory"
   
   if not os.path.exists(path):
    try: 
        parent_directory = os.path.dirname(path)
        os.makedirs(parent_directory, exist_ok=True)
    except Exception as e:
        return f"Error: {e}"
   
   try:
       with open(path,'w') as f:
           f.write(content)
   except Exception as e:
       return f"Error:{e}"
   
   return f"Successfully wrote to '{file_path}' ({len(content)}) characters written"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write or overwrite files constrained to the working directory. ",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path where the file to be overwritten is located, relative to the working directory, if the file does not exist, it creates one relative to the working directory with its respective directory parents"
                ),            
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content which will be overwritten or written in the file specified"
                ),
            },
        required=["file_path", "content"],
        ),
    )