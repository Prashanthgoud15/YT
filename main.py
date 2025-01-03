from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from pytube import YouTube
import os

app = FastAPI()

DOWNLOAD_FOLDER = "./downloads"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.post("/download")
async def download_video(request: Request):
    data = await request.json()
    url = data.get("url")
    format = data.get("format", "mp4")

    if not url:
        raise HTTPException(status_code=400, detail="URL is required.")

    try:
        yt = YouTube(url)
        if format == "mp3":
            stream = yt.streams.filter(only_audio=True).first()
        else:
            stream = yt.streams.filter(progressive=True, file_extension="mp4").first()

        output_file = stream.download(output_path=DOWNLOAD_FOLDER)
        file_name = os.path.basename(output_file)

        return JSONResponse({"success": True, "file_name": file_name, "file_url": f"/files/{file_name}"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/files/{file_name}")
async def get_file(file_name: str):
    file_path = os.path.join(DOWNLOAD_FOLDER, file_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found.")
    return FileResponse(file_path, media_type="application/octet-stream", filename=file_name)
