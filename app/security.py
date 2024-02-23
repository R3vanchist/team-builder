import os
import uuid

def sanitize_filename(filename: str) -> str:
    safe_filename = os.path.basename(filename)
    safe_filename = "".join(char for char in safe_filename if char.isalnum() or char in ['-','_','.'])
    return safe_filename

def generate_filename(original_filename: str, identifier: str) -> str:
    safe_filename = sanitize_filename(original_filename)
    file_extension = os.path.splitext(safe_filename)[1]
    unique_id = uuid.uuid4().hex
    new_filename = f"{identifier}_{unique_id}{file_extension}"
    return new_filename