import os 
import subprocess
from google import genai 
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))
        if os.path.commonpath([abs_working_dir, abs_file_path]) != abs_working_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not abs_file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", abs_file_path]
        if args:
            command.extend(args)
        completed_cmd = subprocess.run(args=command, cwd=abs_working_dir, capture_output=True, timeout=30, text=True)
        if not completed_cmd.stdout and not completed_cmd.stderr:
            return "No output produced"
           
        else:
            output_parts = []
            if completed_cmd.returncode != 0:
                returncode_output = f'Process exited with code {completed_cmd.returncode}'
                output_parts.append(returncode_output)
            if completed_cmd.stdout:
                stdout_string = f'STDOUT: {completed_cmd.stdout}'
                output_parts.append(stdout_string)      
            if completed_cmd.stderr:              
                stderr_string = f'STDERR: {completed_cmd.stderr}'
                output_parts.append(stderr_string)
            output_string = "\n".join(output_parts)
            return output_string
    except Exception as e:
        return f'Error: executing Python file: {e}'
    

    ## SCHEMA FOR THE GET FILES INFO FUNC FOR LLM CALL ##
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a specified Python file within the working directory and returns its output",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to run, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="Optional list of arguments to pass to the Python script",
            ),
        },
        required=["file_path"],
    ),
)