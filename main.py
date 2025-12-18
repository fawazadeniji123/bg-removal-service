import io

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from rembg import remove

app = FastAPI(
    title="Background Removal API",
    description="A simple API to remove backgrounds from images using the rembg library.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    # Configure CORS settings
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/", summary="API Health Check")
async def read_root():
    return {"message": "Background Removal API is running."}


@app.post("/remove-bg", summary="Remove background from an uploaded image")
async def remove_background(file: UploadFile = File(...)):
    # 1. Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File provided is not an image.")

    try:
        # 2. Read image content
        input_image = await file.read()

        # 3. Process the image with rembg
        # Note: rembg handles bytes directly, making it very efficient
        output_image = remove(input_image)

        # 4. Return as a streaming response
        return StreamingResponse(io.BytesIO(output_image), media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
