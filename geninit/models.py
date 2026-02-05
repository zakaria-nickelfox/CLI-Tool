from typing import List
from pydantic import BaseModel, Field

class FileContent(BaseModel):
    path: str = Field(..., description="The relative path of the file including the filename (e.g., 'src/main.py')")
    content: str = Field(..., description="The full code content of the file")

class GeneratedProject(BaseModel):
    files: List[FileContent] = Field(..., description="A list of files to be created in the project")
