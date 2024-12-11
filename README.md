# Edge TTS Web UI

基于 Microsoft Edge 浏览器 TTS 引擎的在线语音合成系统，提供简单易用的 Web 界面。
文本转语音（TTS），字幕生成（SRT）
[English](README_EN.md) | 简体中文
文本转语音

## ✨ 特性

- 🌍 支持多语言：中文（简体、繁体、粤语）、英语、日语等 74 种语言
- 🎭 丰富音色：提供 318 种不同的声音选项 
- 🎛️ 灵活调节：支持语速调整（0.25x-4x）
- 📝 字幕支持：自动生成 SRT 格式字幕
- 🎯 精准同步：音频与字幕完美对齐
- 💾 文件管理：自动清理过期文件
- 🔒 用户隔离：独立的用户空间
- 📱 响应式设计：完美支持移动端


# 更新日志

## [1.1.0] - 2024-01-09

### 新增功能
- 支持 74 种语言和 318 种声音选项
- 添加现代化响应式用户界面
- 新增音频文件缓存系统
- 添加播放历史记录功能
- 实现一键删除音频功能
- 新增音频管理 API 接口
- 添加 Docker 支持，提供容器化部署方案

### 优化改进
- 优化语音选择界面，支持快速切换语言和性别
- 改进音频播放控制，提供实时播放状态
- 优化文件管理系统，提供更好的存储结构
- 完善用户隔离机制，提升数据安全性
- 改进自动清理机制，更高效的资源管理

### 部署更新
- 新增 Dockerfile 用于构建 Docker 镜像
- 新增 docker-compose.yml 简化部署流程
- 添加数据卷配置，支持音频文件持久化
- 支持环境变量配置，如时区设置

### API 更新
- 新增 `/api/audio/list/{user_id}` 接口获取用户音频列表
- 新增 `/api/audio/{audio_id}` 接口删除指定音频
- 优化 `/api/voices` 接口，支持语言和性别筛选
- 完善 `/api/generate` 接口参数说明

## 📸 演示

![主界面](screenshots/main.png)
*主界面*

![语音合成](screenshots/synthesis.png)
*语音合成过程*

![移动端](screenshots/mobile.png)
*移动端适配*

## 🚀 快速开始

1. 克隆项目
```bash
git clone https://github.com/D6397/edge-tts-web-ui.git
cd edge-tts-web-ui
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 启动服务
```bash
python app.py
```

访问 http://localhost:8005 即可使用

#### 使用 docker-compose（推荐）
1. 克隆项目
```bash
git clone https://github.com/D6397/edge-tts-web-ui.git
cd edge-tts-web
```

2. 启动服务
```bash
docker-compose up -d
```

3. 访问服务
```
http://localhost:8005
```

#### 手动构建 Docker 镜像
1. 构建镜像
```bash
docker build -t edge-tts-web .
```

2. 运行容器
```bash
docker run -d \
  --name edge-tts-web \
  -p 8005:8005 \
  -v $(pwd)/static/audio:/app/static/audio \
  edge-tts-web
```

3. 访问服务
```
http://localhost:8005

## 📝 API 文档

启动服务后访问：
- Swagger UI: http://localhost:8005/docs
- ReDoc: http://localhost:8005/redoc

### 主要接口

- `GET /api/voices` - 获取可用声音列表
- `POST /api/generate` - 生成语音文件
- `GET /api/audio/{user_id}` - 获取用户音频列表
- `GET /api/subtitle/{audio_id}` - 获取字幕文件

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

本项目采用 MIT 许可证

## 🙏 鸣谢

- [Edge-TTS](https://github.com/rany2/edge-tts) - TTS 引擎支持
- [FastAPI](https://fastapi.tiangolo.com/) - Web 框架

