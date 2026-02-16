from io import BytesIO
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from rembg import remove

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
async def remove_bg(file: UploadFile = File(...)):
    input_data = await file.read()
    
    # Use the 'u2netp' model (the 'p' stands for 'portable/small')
    # This uses significantly less RAM than the default model.
    output_data = remove(input_data, session_name="u2netp")
    
    return StreamingResponse(io.BytesIO(output_data), media_type="image/png")