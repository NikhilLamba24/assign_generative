import os
from typing import Any, Optional
from crewai.tools import BaseTool
from pydantic import BaseModel


class FileReaderToolInput(BaseModel):
    '''
    parameter handling
    '''
    filename: str
    directory: Optional[str] = "./"  # Default to current directory


class FileReaderTool(BaseTool):
    '''This is the main function to be called by the user in search of file reader tool.
    Expectation:
                filename: enter the filename that you want to read from
                directory: enter the directory path of this file
    '''
    name: str = "File Reader Tool"
    description: str = (
        "A tool to read content from a specified file. Accepts filename and optionally a directory path."
    )
    args_schema = FileReaderToolInput

    def _run(self, **kwargs: Any) -> str:
        try:
            # curating complete path for file
            filepath = os.path.join(kwargs.get("directory") or "", kwargs["filename"])

            # checking for file's existence
            if not os.path.exists(filepath):
                return f"Error: The file {filepath} does not exist."

            # utf encoded content reading
            with open(filepath, "r", encoding="utf-8") as file:
                content = file.read()

            return content  # returning the content read

        except Exception as e:
            return f"An error occurred while reading the file: {str(e)}"
