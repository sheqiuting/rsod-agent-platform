\# RSOD Agent Platform - 基于YOLOv11的目标检测智能体平台



\## 项目简介

基于 YOLOv11 与 LangChain/LangGraph 智能体架构的遥感目标检测平台，支持图像/视频/摄像头多种检测模式，并提供智能对话交互。



\## 技术栈

\- \*\*后端\*\*: Python 3.11 + FastAPI + LangChain + LangGraph + YOLOv11

\- \*\*前端\*\*: Vue 3 + Vite + Element Plus + ECharts

\- \*\*基础设施\*\*: PostgreSQL + Redis + MinIO + Docker Compose



\## 快速启动

```bash

\# 启动基础设施

docker compose up -d



\# 启动后端

cd backend

.venv\\Scripts\\activate

py main.py



\# 启动前端

cd frontend

npm run dev

访问地址
前端页面: http://localhost:5173
API 文档: http://localhost:8000/docs
MinIO 控制台: http://localhost:9001