import streamlit as st
import pandas as pd
import tempfile
import os
from pathlib import Path
from typing import Dict, Any

class FileHandler:
    """Handle file uploads and validation for financial documents"""
    
    SUPPORTED_FORMATS = {
        'pdf': ['pdf'],
        'excel': ['xlsx', 'xls', 'xlsm']
    }
    
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB limit
    
    @staticmethod
    def validate_file(uploaded_file) -> Dict[str, Any]:
        """Validate uploaded file format and size"""
        if uploaded_file is None:
            return {"valid": False, "error": "No file uploaded"}
        
        if uploaded_file.size > FileHandler.MAX_FILE_SIZE:
            return {"valid": False, "error": f"File too large. Max size: 50MB"}
        
        file_extension = Path(uploaded_file.name).suffix.lower().lstrip('.')
        
        supported_extensions = []
        for format_type, extensions in FileHandler.SUPPORTED_FORMATS.items():
            supported_extensions.extend(extensions)
        
        if file_extension not in supported_extensions:
            return {"valid": False, "error": f"Unsupported format. Supported: {', '.join(supported_extensions)}"}
        
        return {
            "valid": True, 
            "file_type": FileHandler._get_file_type(file_extension),
            "extension": file_extension,
            "size": uploaded_file.size,
            "name": uploaded_file.name
        }
    
    @staticmethod
    def _get_file_type(extension: str) -> str:
        """Determine file type from extension"""
        for file_type, extensions in FileHandler.SUPPORTED_FORMATS.items():
            if extension in extensions:
                return file_type
        return "unknown"
    
    @staticmethod
    def save_temp_file(uploaded_file) -> str:
        """Save uploaded file to temporary location"""
        temp_dir = tempfile.mkdtemp()
        temp_path = os.path.join(temp_dir, uploaded_file.name)
        
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        return temp_path
