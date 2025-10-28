import json
from fastapi import FastAPI, File, UploadFile, Form, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
from image_ops import apply_operation  # changed from relative import

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/process")
async def process_image(
    file: UploadFile = File(...),
    operation: str = Form(...),
    params: str = Form("{}"),
):
    try:
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("Could not decode image")

        params_dict = json.loads(params) if params else {}
        result = apply_operation(img, operation, params_dict)

        success, encoded_img = cv2.imencode(".png", result)
        if not success:
            raise ValueError("Failed to encode result image")

        return Response(content=encoded_img.tobytes(), media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
