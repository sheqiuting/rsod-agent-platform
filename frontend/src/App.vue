<template>
  <div id="app">
    <h1>🔍 YOLOv11 目标检测</h1>

    <div class="upload-area" @dragover.prevent @drop.prevent="handleDrop">
      <input
        type="file"
        accept="image/*"
        @change="handleFileChange"
        ref="fileInput"
      />
      <button @click="$refs.fileInput.click()">📤 选择图片</button>
      <p v-if="fileName">已选择：{{ fileName }}</p>
    </div>

    <button
      @click="detect"
      :disabled="!selectedFile || loading"
      class="detect-btn"
    >
      {{ loading ? "检测中..." : "🚀 开始检测" }}
    </button>

    <div v-if="result" class="result-container">
      <h2>检测结果（共 {{ result.total_objects }} 个目标）</h2>
      <div class="image-wrapper">
        <img :src="imagePreview" ref="imageRef" @load="drawBoxes" />
        <canvas
          ref="canvasRef"
          :width="canvasWidth"
          :height="canvasHeight"
        ></canvas>
      </div>
      <ul class="detection-list">
        <li v-for="(item, idx) in result.detections" :key="idx">
          <span class="label">{{ item.label }}</span>
          <span class="confidence">置信度: {{ item.confidence }}</span>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      selectedFile: null,
      fileName: "",
      imagePreview: null,
      result: null,
      loading: false,
      canvasWidth: 800,
      canvasHeight: 600,
    };
  },
  methods: {
    handleFileChange(e) {
      const file = e.target.files[0];
      if (file) {
        this.selectedFile = file;
        this.fileName = file.name;
        this.imagePreview = URL.createObjectURL(file);
        this.result = null;
      }
    },
    handleDrop(e) {
      const file = e.dataTransfer.files[0];
      if (file) {
        this.selectedFile = file;
        this.fileName = file.name;
        this.imagePreview = URL.createObjectURL(file);
        this.result = null;
      }
    },
    async detect() {
      if (!this.selectedFile) return;
      this.loading = true;
      this.result = null;

      const formData = new FormData();
      formData.append("file", this.selectedFile);

      try {
        const response = await axios.post("/detect", formData, {
          headers: { "Content-Type": "multipart/form-data" },
        });
        this.result = response.data;
        console.log("检测结果:", this.result);
        this.$nextTick(() => {
          this.drawBoxes();
        });
      } catch (error) {
        console.error("检测失败:", error);
        alert("检测失败，请检查后端服务是否启动");
      } finally {
        this.loading = false;
      }
    },
    drawBoxes() {
      const img = this.$refs.imageRef;
      const canvas = this.$refs.canvasRef;
      if (!img || !canvas || !this.result) {
        console.log("drawBoxes: 缺少必要的元素");
        return;
      }
      console.log("drawBoxes: 绘制", this.result.detections.length, "个检测框");

      const rect = img.getBoundingClientRect();
      canvas.width = rect.width;
      canvas.height = rect.height;
      this.canvasWidth = rect.width;
      this.canvasHeight = rect.height;

      const ctx = canvas.getContext("2d");
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      this.result.detections.forEach((item) => {
        const [x1, y1, x2, y2] = item.bbox;
        const scaleX = canvas.width / img.naturalWidth;
        const scaleY = canvas.height / img.naturalHeight;

        ctx.strokeStyle = "#00FF00";
        ctx.lineWidth = 3;
        ctx.strokeRect(
          x1 * scaleX,
          y1 * scaleY,
          (x2 - x1) * scaleX,
          (y2 - y1) * scaleY,
        );

        ctx.fillStyle = "#00FF00";
        const label = `${item.label} ${item.confidence}`;
        ctx.font = "16px Arial";
        const metrics = ctx.measureText(label);
        const padding = 4;
        const textX = x1 * scaleX;
        const textY = y1 * scaleY - 20;
        ctx.fillRect(textX, textY, metrics.width + padding * 2, 20);

        ctx.fillStyle = "#000000";
        ctx.fillText(label, textX + padding, textY + 15);
      });
    },
  },
};
</script>

<style scoped>
#app {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
  text-align: center;
}
.upload-area {
  border: 2px dashed #aaa;
  border-radius: 12px;
  padding: 30px;
  margin: 20px 0;
  background: #f9f9f9;
}
.upload-area input[type="file"] {
  display: none;
}
.upload-area button {
  background: #4caf50;
  color: white;
  border: none;
  padding: 10px 24px;
  border-radius: 6px;
  font-size: 16px;
  cursor: pointer;
}
.upload-area button:hover {
  background: #45a049;
}
.detect-btn {
  background: #2196f3;
  color: white;
  border: none;
  padding: 12px 36px;
  border-radius: 6px;
  font-size: 18px;
  cursor: pointer;
  margin: 10px 0;
}
.detect-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}
.result-container {
  margin-top: 30px;
  text-align: left;
}
.image-wrapper {
  position: relative;
  display: inline-block;
  width: 100%;
}
.image-wrapper img {
  width: 100%;
  display: block;
  border-radius: 8px;
}
.image-wrapper canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  border-radius: 8px;
}
.detection-list {
  list-style: none;
  padding: 0;
  margin-top: 15px;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}
.detection-list li {
  background: #e8f5e9;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 14px;
}
.detection-list .label {
  font-weight: bold;
  margin-right: 8px;
}
.detection-list .confidence {
  color: #555;
}
</style>
