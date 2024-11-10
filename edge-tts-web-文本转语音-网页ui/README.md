# Edge TTS Web

[![License](https://img.shields.io/github/license/your-username/edge-tts-web)](https://github.com/your-username/edge-tts-web/blob/main/LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68+-green.svg)](https://fastapi.tiangolo.com/)
[![Edge-TTS](https://img.shields.io/badge/Edge--TTS-6.1.9-orange.svg)](https://github.com/rany2/edge-tts)

基于 Microsoft Edge 浏览器 TTS 引擎的在线语音合成系统，提供简单易用的 Web 界面。

[English](README_EN.md) | 简体中文

## ✨ 特性

- 🌍 支持 74 种语言，318 种声音选项
- 🎯 中文支持：普通话、粤语、闽南语等多种方言
- 🎨 简洁美观的用户界面
- ⚡ 快速的语音合成速度
- 📝 自动生成字幕文件（SRT格式）
- 🎚️ 可调节语速 (0.25x-4x)
- 🔄 自动清理过期文件
- 📱 响应式设计，支持移动端

## 🚀 快速开始

```

### 手动安装

1. 克隆项目
```bash
git clone https://github.com/your-username/edge-tts-web.git
cd edge-tts-web
```

2. 安装依赖
```bash
pip install fastapi uvicorn edge-tts python-multipart mutagen
```

3. 启动服务
```bash
python app.py
```

访问 http://localhost:8005 即可使用

详细安装说明请参考 [安装指南](INSTALL.md)

## 📸 截图

![Screenshot](screenshots/main.png)

## 🔧 配置说明

- 默认端口：8005
- 音频存储路径：static/audio
- 自动清理：30分钟后自动删除音频文件
- 支持跨域：默认允许所有源

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

欢迎贡献代码！请查看 [贡献指南](CONTRIBUTING.md)。

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 鸣谢

- [Edge-TTS](https://github.com/rany2/edge-tts) - TTS 引擎支持
- [FastAPI](https://fastapi.tiangolo.com/) - Web 框架
- [TailwindCSS](https://tailwindcss.com/) - UI 样式

## 📞 联系方式

- 提交 Issue: [GitHub Issues](https://github.com/your-username/edge-tts-web/issues)
- 邮箱: your-email@example.com

## 🌟 Star 历史

[![Star History Chart](https://api.star-history.com/svg?repos=your-username/edge-tts-web&type=Date)](https://star-history.com/#your-username/edge-tts-web&Date)
