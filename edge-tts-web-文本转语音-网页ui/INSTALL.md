# 安装指南

## 系统要求

- Python 3.7+
- pip 包管理器
- 足够的磁盘空间用于存储音频文件

## 安装步骤

1. 克隆项目
```bash
git clone https://github.com/your-repo/edge-tts-web.git
cd edge-tts-web
```

2. 创建虚拟环境（推荐）
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. 安装依赖
```bash
pip install fastapi uvicorn edge-tts python-multipart mutagen
```

4. 创建必要的目录
```bash
mkdir -p static/audio
```

5. 启动服务
```bash
python app.py
```

或使用 uvicorn：
```bash
uvicorn app:app --host 0.0.0.0 --port 8005 --reload
```

## Docker 部署

1. 构建镜像
```bash
docker build -t edge-tts-web .
```

2. 运行容器
```bash
docker run -d \
  --name edge-tts-web \
  -p 8005:8005 \
  -v /path/to/audio:/app/static/audio \
  edge-tts-web
```

## 配置说明

1. 端口配置
- 默认端口为 8005
- 可在 app.py 中修改或通过环境变量设置

2. 存储配置
- 音频文件存储在 static/audio 目录
- 建议配置定期清理机制

3. 跨域配置
- 默认允许所有源
- 可在 app.py 中的 CORS 配置部分修改

## 常见问题

1. 依赖安装失败
```bash
# 尝试更新 pip
python -m pip install --upgrade pip

# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

2. 端口被占用
```bash
# 修改端口号
uvicorn app:app --host 0.0.0.0 --port 8006 --reload
```

3. 权限问题
```bash
# 确保有写入权限
chmod -R 755 static/audio
```

## 更新说明

定期检查项目更新：
```bash
git pull origin main
pip install -r requirements.txt
```