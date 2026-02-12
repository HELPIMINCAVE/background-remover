from fastapi import FastAPI, UploadFile, File, Response
from rembg import remove
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all websites to access the API (fine for local dev)
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
    input_image = await file.read()
    
    # Process the image
    output_image = remove(input_image)
    
    # RETURN AS A PROPER IMAGE RESPONSE
    return Response(content=output_image, media_type="image/png")