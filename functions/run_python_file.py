import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path,args=None):

    path = os.path.join(working_directory,file_path)

    if not os.path.abspath(path).startswith(os.path.abspath(working_directory)):
        return f"Error: Cannot execute '{file_path}' as it is outside the permitted working directory"

    if not os.path.exists(path):
        return f'Error: File "{file_path}" not found.'
    
    if not path.endswith(".py"):
        return f'Error: "{path}" is not a Python file'
    
    try:
        commands = ["python",path]
        if args:
            commands.append(args)

        file_execute = subprocess.run(commands,capture_output=True, text=True, timeout=30, cwd=os.path.abspath(working_directory))
        output = []

        if file_execute.stdout:
            output.append(f"STDOUT:\n{file_execute.stdout}")
        if file_execute.stderr:
            output.append(f"STDERR:\n{file_execute.stderr}")
        if file_execute.returncode != 0 :
            output.append(f"Process exited with code {file_execute.returncode}")

        return "\n".join(output) if output else "No output produced"
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute Python files with optional arguments. It only executes files which have an extension of .py constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path where the file to be executed is located, relative to the working directory."
                ),
            },
        ),
    )