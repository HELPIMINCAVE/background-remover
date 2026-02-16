from io import BytesIO
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from rembg import remove

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows local files (origin 'null') to connect
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/remove-bg")
async def remove_background(file: UploadFile = File(...)):
    # Read the uploaded image
    input_data = await file.read()
    
    # Use rembg to remove the background
    output_data = remove(input_data)
    
    # Return the processed image as a response
    return StreamingResponse(BytesIO(output_data), media_type="image/png")