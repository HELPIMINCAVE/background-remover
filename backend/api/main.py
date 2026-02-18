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
async def remove_background(file: UploadFile = File(...)):
    input_data = await file.read()
    # The session_name="u2netp" forces the 4MB model instead of the 176MB one
    output_data = remove(input_data, session_name="u2netp")
    return StreamingResponse(BytesIO(output_data), media_type="image/png")