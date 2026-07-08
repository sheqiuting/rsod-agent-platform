import axios from "axios";

const request = axios.create({
  baseURL: "/api",
  timeout: 30000,
  headers: {
    "Content-Type": "application/json",
  },
});

// 请求拦截器 ———— 在这里添加 Token
request.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("rsod_token");
    console.log("🔍 拦截器获取到的 Token:", token); // 临时调试日志
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
      console.log("✅ 已设置 Authorization 头");
    } else {
      console.log("❌ 没有 Token");
    }
    return config;
  },
  (error) => Promise.reject(error),
);

// 响应拦截器
request.interceptors.response.use(
  (response) => response.data,
  (error) => {
    // ... 错误处理保持不变
    return Promise.reject(error);
  },
);

export default request;
