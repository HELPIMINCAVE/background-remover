from io import BytesIO
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from rembg import remove, new_session

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex='.*',  # This is a "catch-all" for any origin, including null
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/remove-bg")
async def remove_background(file: UploadFile = File(...)):
    input_data = await file.read()
    
    # 1. Manually create a tiny session
    session = new_session("u2netp")
    
    # 2. Use that specific session to process the image
    output_data = remove(input_data, session=session)
    
    return StreamingResponse(BytesIO(output_data), media_type="image/png")