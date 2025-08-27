# from fastapi import FastAPI, UploadFile, Form
# from fastapi.responses import FileResponse
# from workflows.slide_workflow import build_workflow
# import os

# app = FastAPI()

# @app.get("/health")
# def health():
#     return {"status": "ok"}

# @app.post("/generate_slides")
# async def generate_slides(topic: str = Form(...)):
#     pptx_file = build_workflow(topic)
#     return FileResponse(pptx_file, media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
#                         filename=f"{topic}_slides.pptx")


# @app.post("/upload_doc")
# async def upload_doc(file: UploadFile):
#     temp_path = f"temp_{file.filename}"
#     with open(temp_path, "wb") as f:
#         f.write(await file.read())

#     # For now: just use the filename as text (dummy)
#     pptx_file = build_workflow(f"Document uploaded: {file.filename}")

#     return FileResponse(pptx_file, filename="slides.pptx")

import __main__
from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from workflows.slide_workflow import build_workflow

import os
import tempfile
import logging

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title =  "SlideMage",
    description = "AI-powered presentation generation service",
    version = "1.0.0"   
)

app.add_middleware(
    CORSMiddleware,
    allow_origins  = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

@app.post("/generate_slides")
async def generate_slides(topic: str = Form(...)):
    try: 
        if not topic.strip():
            raise HTTPException(status_code=400, detail="Topic cannot be empty")
        
        logger.info(f"Generating slides for topic: {topic}")
        pptx_file = build_workflow(topic)

        if not os.path.exists(pptx_file):
            raise HTTPException(status_code=500, detail="Failed to generate presentation")
        
        return FileResponse(pptx_file, media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                            filename=f"{topic}_slides.pptx")
    
    except Exception as e:
        logger.error(f"Error generating slides: {e}")
        raise HTTPException(status_code = 500, detail = f"Error generating slides: {str(e)}")


@app.post("/upload_doc")
async def upload_doc(file: UploadFile):
    try:
        allowed_types = ["text/plain", "application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
        if file.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail="Unsupported file type")
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{file.filename}") as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_path = temp_file.name
        
        try:
            topic = f"Document: {file.filename}"
            pptx_file = build_workflow(topic)
            
            return FileResponse(
                pptx_file, 
                media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                filename=f"{file.filename}_slides.pptx"
            )
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
                
    except Exception as e:
        logger.error(f"Error processing document: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")


if __name__ == "__main__":
    import uvicorn



