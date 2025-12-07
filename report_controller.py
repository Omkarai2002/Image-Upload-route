import os
import re
import shutil
import subprocess
from typing import List

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from dotenv import load_dotenv

from auth_middleware import auth
import config
load_dotenv()

router = APIRouter()
BASE_DIR = os.getenv("BASE_PATH")


@router.post("/upload-images")
async def upload_images(
    reportName: str = Form(...),
    files: List[UploadFile] = File(...),
    user_data: dict = Depends(auth),
):
    if not files or len(files) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least 1 image is required",
        )

    if not reportName:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Report name is required",
        )

    user_id = user_data.get("userId")
    # console.log("userId" , user_id);
    if user_id==12:
        remote_dir=config.CONF[12]
    elif user_id==13:
        remote_dir=config.CONF[13]
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User authentication failed",
        )

    remote_dir = os.path.join(remote_dir, reportName)

    try:
        os.makedirs(remote_dir, exist_ok=True)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error creating directory: {str(e)}"
        )

    uploaded_files = []

    try:
        for file in files:
            safe_file_name = re.sub(r"[^\w\.-]", "_", file.filename or "file")
            remote_file_path = os.path.join(remote_dir, safe_file_name)

            with open(remote_file_path, "wb") as f:
                shutil.copyfileobj(file.file, f)

            uploaded_files.append(safe_file_name)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error saving files: {str(e)}"
        )

    try:
        if len(uploaded_files)>=1:
            script_cmd = ["bash", "home/ubuntu/myscript.sh", str(user_id)]
            subprocess.Popen(
                script_cmd,
                cwd=BASE_DIR,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Uploaded but script failed: {str(e)}"
        )

    return {
        "success": True,
        "message": "Images uploaded & script started successfully",
        "data": {
            "reportName": reportName,
            "filesUploaded": len(uploaded_files),
            "files": uploaded_files,
        },
    }
