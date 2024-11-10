于 Microsoft Edge 浏览器 TTS 引擎的在线语音合成系统，提供简单易用的 Web 界面。
文本转语音（TTS），字幕生成（SRT）
[English](README_EN.md) | 简体中文

## ✨ 特性

- 🌍 支持多语言：中文（简体、繁体、粤语）、英语、日语等 74 种语言
- 🎭 丰富音色：提供 318 种不同的声音选项 
- 🎛️ 灵活调节：支持语速调整（0.25x-4x）
- 📝 字幕支持：自动生成 SRT 格式字幕
- 🎯 精准同步：音频与字幕完美对齐
- 💾 文件管理：自动清理过期文件
- 🔒 用户隔离：独立的用户空间
- 📱 响应式设计：完美支持移动端

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
git clone https://github.com/bu950223/edge-tts-web----ui.git
cd edge-tts-web----ui
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

