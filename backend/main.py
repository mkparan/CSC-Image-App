# activity/Back-end/main.py
import io
import json
import zipfile
import tempfile
from typing import List

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

import image_ops

app = FastAPI(title="CSC Image Processing API")

# For development allow all origins (Electron runs file:///). For production tighten this.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health():
    return {"status": "ok", "service": "CSC Image Processing API"}


@app.get("/operations")
def operations():
    """Return available operations and their parameter descriptions."""
    return image_ops.get_operations()


@app.post("/process")
async def process(
    file: UploadFile = File(...),
    operation: str = Form(...),
    params: str = Form("{}"),
):
    """
    Process a single image.
    - file: image file
    - operation: operation name as string
    - params: JSON string with operation-specific parameters
    """
    try:
        body = await file.read()
        params_obj = json.loads(params or "{}")
        out_bytes, mime = image_ops.process_image(body, operation, params_obj)
        return StreamingResponse(io.BytesIO(out_bytes), media_type=mime)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/batch_process")
async def batch_process(
    files: List[UploadFile] = File(...),
    operation: str = Form(...),
    params: str = Form("{}"),
):
    """
    Process multiple images and return a zip file of results.
    """
    try:
        params_obj = json.loads(params or "{}")
        tmp = tempfile.TemporaryFile()
        with zipfile.ZipFile(tmp, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
            for idx, f in enumerate(files):
                body = await f.read()
                out_bytes, mime = image_ops.process_image(body, operation, params_obj)
                # ensure filename
                name = f"result_{idx + 1}.png"
                zf.writestr(name, out_bytes)
        tmp.seek(0)
        headers = {"Content-Disposition": "attachment; filename=results.zip"}
        return StreamingResponse(tmp, media_type="application/zip", headers=headers)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
