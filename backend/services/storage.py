import os
import shutil
import uuid
import asyncio
from fastapi import UploadFile
import cloudinary
import cloudinary.uploader

# Configure Cloudinary
# If these env vars are missing, we fall back to local storage
CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

USE_CLOUD = all([CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET])

if USE_CLOUD:
    cloudinary.config( 
        cloud_name = CLOUDINARY_CLOUD_NAME, 
        api_key = CLOUDINARY_API_KEY, 
        api_secret = CLOUDINARY_API_SECRET,
        secure = True
    )

# Local storage setup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Go up one level from services/
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

class StorageService:
    @staticmethod
    async def upload_file(file: UploadFile, base_url: str = "http://localhost:8000") -> str:
        """
        Uploads a file to Cloudinary (if configured) or Local Storage.
        Returns the public URL of the uploaded file.
        """
        if USE_CLOUD:
            return await StorageService._upload_to_cloudinary(file)
        else:
            return await StorageService._upload_local(file, base_url)

    @staticmethod
    async def _upload_to_cloudinary(file: UploadFile) -> str:
        # Read file into memory
        content = await file.read()
        
        def upload_sync():
            # Cloudinary upload accepts file-like object or byte array
            response = cloudinary.uploader.upload(content, folder="the-set-web")
            return response["secure_url"]

        # Run blocking upload in thread
        return await asyncio.to_thread(upload_sync)

    @staticmethod
    async def _upload_local(file: UploadFile, base_url: str) -> str:
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        # Reset file cursor just in case
        await file.seek(0)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        return f"{base_url}/static/{unique_filename}"
