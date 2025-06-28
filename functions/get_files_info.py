import os

def get_files_info(working_directory, directory=None):

    path = os.path.join(working_directory,directory)

    if directory.startswith(".") and "../" not in directory:
        directory= working_directory
        path = directory
    
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


def get_file_content(working_directory, file_path):
    path = os.path.join(working_directory,file_path)

    print(os.path.abspath(path).startswith(os.path.abspath(working_directory)))

    if not os.path.abspath(path).startswith(os.path.abspath(working_directory)):
        return f"Error: Cannot read '{file_path}' as it is outside the permitted working directory"

    if not os.path.isfile(path):
        return f"Error: File not found or is not a regular file: '{file_path}'"
    return "En Proceso"


def read_file(file):
    MAX_CHARS = 10000
    try:
        with open(file,"r") as f:
            string_text = f.read(MAX_CHARS)
            return string_text if len(string_text)<MAX_CHARS else string_text + f"...File '{file}' truncated at 10000 characters"
    except Exception as e:
        return f"Error: {e}"