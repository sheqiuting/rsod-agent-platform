from contextlib import asynccontextmanager
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
import numpy as np
import io
from PIL import Image

from app.config.settings import settings
from app.api.auth import router as auth_router

@asynccontextmanager
async def lifespan(_app: FastAPI):
    print("正在初始化服务...")
    yield
    print("服务已关闭")

app = FastAPI(
    title="RSOD Agent Platform",
    version="0.1.0",
    description="基于 YOLOv11 的目标检测智能体平台 API",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册认证路由
app.include_router(auth_router)

# ===== 原有路由 =====
@app.get("/")
def root():
    return {"message": "欢迎使用 RSOD Agent Platform", "version": "0.1.0", "docs": "/docs"}

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "app_name": "RSOD Agent Platform", "version": "0.1.0"}

model = YOLO("yolo11n.pt")

@app.post("/detect")
async def detect_objects(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    image_np = np.array(image)
    results = model(image_np)
    detections = []
    for result in results:
        boxes = result.boxes
        if boxes is not None:
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                conf = float(box.conf[0])
                cls = int(box.cls[0])
                label = model.names[cls]
                detections.append({
                    "label": label,
                    "confidence": round(conf, 3),
                    "bbox": [round(x1, 2), round(y1, 2), round(x2, 2), round(y2, 2)]
                })
    return {
        "filename": file.filename,
        "detections": detections,
        "total_objects": len(detections)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
