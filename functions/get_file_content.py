import os

from config import char_limit


def get_file_content(working_directory, file_path):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))
        if os.path.commonpath([abs_working_dir, abs_file_path]) != abs_working_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(abs_file_path, "r") as f:
            content = f.read(char_limit)
            if f.read(1):
                content += (
                    f'[...File "{file_path}" truncated at {char_limit} characters]'
                )
        return content
    except Exception as e:
        return f'Error reading file "{file_path}": {e}'