from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, FileResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import edge_tts
import asyncio
import uuid
import os
from typing import List, Optional
import json
from mutagen.mp3 import MP3
import time
from datetime import datetime, timedelta

app = FastAPI()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# 配置静态文件服务
os.makedirs("static/audio", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# 添加根路径处理
@app.get("/")
async def read_root():
    return FileResponse('index.html')

# 修改 favicon 处理部分
@app.get('/favicon.ico')
async def favicon():
    try:
        # 直接使用网站根目录的 favicon.ico
        favicon_path = '/www/wwwroot/favicon.ico'
        if os.path.exists(favicon_path):
            return FileResponse(
                favicon_path,
                media_type="image/x-icon"
            )
        else:
            print(f"Favicon not found at: {favicon_path}")
            raise HTTPException(status_code=404, detail="Favicon not found")
    except Exception as e:
        print(f"Error serving favicon: {str(e)}")
        raise HTTPException(status_code=404, detail="Favicon not found")

# 在 app.mount 之前添加静态文件路由
@app.get("/static/{file_path:path}")
async def static_files(file_path: str):
    return FileResponse(f"static/{file_path}")

class TTSRequest(BaseModel):
    text: str
    voice_id: str
    speed: float = 1.0
    autoplay: bool = True
    user_id: str

class Voice(BaseModel):
    id: str
    name: str
    gender: str
    language: str

# 缓存可用的声音列表
VOICE_CACHE = {}

async def get_voices():
    try:
        if not VOICE_CACHE:
            print("Fetching voices from edge-tts...")
            voices = await edge_tts.list_voices()
            print(f"Got {len(voices)} voices from edge-tts")
            
            for voice in voices:
                lang = voice["Locale"]
                if lang not in VOICE_CACHE:
                    VOICE_CACHE[lang] = []
                
                # 添加更友好的声音名称
                friendly_name = {
                    # 中文声音
                    "zh-CN-XiaoxiaoNeural": "晓晓 (年轻女声)",
                    "zh-CN-XiaoyiNeural": "晓伊 (少女声)",
                    "zh-CN-YunjianNeural": "云健 (年轻男声)",
                    "zh-CN-YunxiNeural": "云希 (少年声)",
                    "zh-CN-YunxiaNeural": "云夏 (男童声)",
                    "zh-CN-YunyangNeural": "云扬 (新闻播音)",
                    "zh-CN-liaoning-XiaobeiNeural": "晓北 (东北女声)",
                    "zh-HK-HiuGaaiNeural": "晓佳 (港式女声)",
                    "zh-HK-HiuMaanNeural": "晓曼 (港式女声)",
                    "zh-HK-WanLungNeural": "云龙 (港式男声)",
                    "zh-TW-HsiaoChenNeural": "晓辰 (台湾女声)",
                    "zh-TW-YunJheNeural": "云哲 (台湾男声)",
                    "zh-TW-HsiaoYuNeural": "晓雨 (台湾女声)",
                    # 英文声音
                    "en-US-JennyNeural": "Jenny (美式女声)",
                    "en-US-GuyNeural": "Guy (美式男声)",
                    "en-GB-SoniaNeural": "Sonia (英式女声)",
                    "en-GB-RyanNeural": "Ryan (英式男声)",
                    # 日文声音
                    "ja-JP-NanamiNeural": "七海 (日本女声)",
                    "ja-JP-KeitaNeural": "圭太 (日本男声)",
                }.get(voice["ShortName"], voice["ShortName"])
                
                print(f"Adding voice: {friendly_name} ({voice['ShortName']})")
                
                VOICE_CACHE[lang].append({
                    "id": voice["ShortName"],
                    "name": friendly_name,
                    "gender": voice["Gender"].lower(),
                    "language": lang
                })
        return VOICE_CACHE
    except Exception as e:
        print(f"Error in get_voices: {str(e)}")
        raise

@app.get("/api/voices")
async def list_voices(language: str = "zh-CN", gender: Optional[str] = None):
    try:
        print(f"Fetching voices for language: {language}, gender: {gender}")
        voices = await get_voices()
        print(f"Available languages: {list(voices.keys())}")
        
        # 获取所有匹配语言前缀的声音
        filtered_voices = []
        for lang, voice_list in voices.items():
            print(f"Checking language: {lang}")
            if lang.startswith(language):
                filtered_voices.extend(voice_list)
        
        print(f"Found {len(filtered_voices)} voices before gender filter")
        
        if gender:
            filtered_voices = [v for v in filtered_voices if v["gender"] == gender.lower()]
            print(f"Found {len(filtered_voices)} voices after gender filter")
        
        # 打印找到的声音
        for voice in filtered_voices:
            print(f"Voice: {voice['name']} ({voice['id']})")
        
        return filtered_voices
    except Exception as e:
        print(f"Error in list_voices: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# 添加时长格式化函数
def format_duration(seconds):
    """将秒数转换为 MM:SS 格式"""
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"

@app.post("/api/generate")
async def generate_audio(request: TTSRequest):
    try:
        # 验证请求参数
        if not request.text:
            raise ValueError("文本内容不能为空")
        if not request.voice_id:
            raise ValueError("未选择声音")
            
        # 生成文件名时包含用户ID
        filename = f"{request.user_id}_{str(uuid.uuid4())}"
        audio_path = f"static/audio/{filename}.mp3"
        subtitle_path = f"static/audio/{filename}.srt"
        
        try:
            print(f"Starting audio generation...")
            print(f"Text: {request.text[:100]}...")
            print(f"Voice ID: {request.voice_id}")
            print(f"Speed: {request.speed}")
            
            # 确保目录存在
            os.makedirs("static/audio", exist_ok=True)
            
            # 修改语速格式
            speed_percentage = int((request.speed - 1) * 100)
            rate = f"{speed_percentage:+d}%"
            print(f"Calculated rate: {rate}")
            
            try:
                # 设置语音参数并生成
                communicate = edge_tts.Communicate(
                    text=request.text,
                    voice=request.voice_id,
                    rate=rate
                )
                print("Created communicate object")

                # 生成音频和字幕
                print(f"Saving audio to: {audio_path}")
                audio_data = []
                subtitle_data = []
                subtitle_index = 1
                
                # 用于合并字幕的临时存储
                temp_text = []
                temp_start = None
                temp_end = None
                
                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        audio_data.append(chunk["data"])
                    elif chunk["type"] == "WordBoundary":
                        # 转换时间戳
                        start_ms = int(chunk['offset'] / 10000)
                        duration_ms = int(chunk['duration'] / 10000)
                        end_ms = start_ms + duration_ms
                        
                        # 如果是新的字幕组或时间间隔太大，就保存当前组
                        if temp_start is None:
                            temp_start = start_ms
                            temp_end = end_ms
                            temp_text.append(chunk["text"])
                        elif end_ms - temp_end > 500:  # 如果间隔超过500毫秒，就作为新的字幕
                            # 保存当前字幕组
                            start_time = format_time(temp_start)
                            end_time = format_time(temp_end)
                            
                            subtitle_entry = [
                                f"{subtitle_index}",
                                f"{start_time} --> {end_time}",
                                "".join(temp_text),
                                ""
                            ]
                            print(f"Adding subtitle entry:\n" + "\n".join(subtitle_entry))
                            subtitle_data.extend(subtitle_entry)
                            subtitle_index += 1
                            
                            # 开始新的字幕组
                            temp_text = [chunk["text"]]
                            temp_start = start_ms
                            temp_end = end_ms
                        else:
                            # 继续当前字幕组
                            temp_text.append(chunk["text"])
                            temp_end = end_ms
                
                # 保存最后一组字幕
                if temp_text:
                    start_time = format_time(temp_start)
                    end_time = format_time(temp_end)
                    subtitle_entry = [
                        f"{subtitle_index}",
                        f"{start_time} --> {end_time}",
                        "".join(temp_text),
                        ""
                    ]
                    print(f"Adding subtitle entry:\n" + "\n".join(subtitle_entry))
                    subtitle_data.extend(subtitle_entry)
                
                # 写入音频文件
                with open(audio_path, "wb") as audio_file:
                    for data in audio_data:
                        audio_file.write(data)

                # 写入 SRT 格式字幕文件
                try:
                    subtitle_content = "\n".join(subtitle_data)
                    print(f"Writing subtitle content:\n{subtitle_content}")
                    
                    with open(subtitle_path, "w", encoding="utf-8", newline='\n') as subtitle_file:
                        subtitle_file.write(subtitle_content)
                        subtitle_file.flush()  # 确保数据写入磁盘
                        os.fsync(subtitle_file.fileno())  # 强制同步到磁盘
                    
                    # 添加短暂延迟确保文件完全写入
                    await asyncio.sleep(0.1)
                    
                    # 验证文件是否正确写入
                    if os.path.exists(subtitle_path):
                        with open(subtitle_path, "r", encoding="utf-8") as check_file:
                            saved_content = check_file.read()
                            print(f"Verified subtitle content:\n{saved_content}")
                            if saved_content != subtitle_content:
                                raise ValueError("Subtitle file content verification failed")
                    else:
                        raise ValueError("Subtitle file was not created")
                    
                    print(f"Subtitle file successfully written to {subtitle_path}")
                    
                except Exception as e:
                    print(f"Error writing subtitle file: {str(e)}")
                    raise

                print("Audio and subtitles saved successfully")
                
                # 再次验证文件是否可访问
                if not (os.path.exists(audio_path) and os.path.exists(subtitle_path)):
                    raise ValueError("Generated files are not accessible")
                
                # 获取文件大小和时长
                file_size = os.path.getsize(audio_path)
                try:
                    # 使用 mutagen 获取音频时长
                    audio = MP3(audio_path)
                    duration = format_duration(audio.info.length)
                    print(f"Audio duration: {duration}")
                except Exception as e:
                    print(f"Error getting audio duration: {str(e)}")
                    duration = "00:00"
                
                return JSONResponse({
                    "success": True,
                    "audio": {
                        "url": f"/static/audio/{filename}.mp3",
                        "name": f"{filename}.mp3",
                        "size": f"{file_size / 1024:.1f}KB",
                        "duration": duration,  # 使用实际计算的时长
                        "id": filename
                    }
                })
                
            except Exception as e:
                print(f"Error during TTS generation: {str(e)}")
                print(f"Error type: {type(e)}")
                import traceback
                print(f"Traceback: {traceback.format_exc()}")
                raise ValueError(f"TTS生成失败: {str(e)}")
            
        except Exception as e:
            print(f"Error in generation process: {str(e)}")
            # 清理可能部分生成的文件
            for path in [audio_path, subtitle_path]:
                if os.path.exists(path):
                    try:
                        os.remove(path)
                        print(f"Cleaned up file: {path}")
                    except Exception as cleanup_error:
                        print(f"Error cleaning up file {path}: {str(cleanup_error)}")
            raise
            
    except Exception as e:
        print(f"Final error handler: {str(e)}")
        error_message = str(e)
        
        # 处理常见错误
        if "Connection refused" in error_message:
            error_message = "无法连接到语音服务，请稍后重试"
        elif "Invalid rate" in error_message:
            error_message = "语速设置无效，请使用正确的语速值"
        elif "Invalid voice" in error_message:
            error_message = "选择的声音无效，请重新选择"
        elif "TTS generation failed" in error_message:
            error_message = "语音生成失败，请重试"
        elif "No such file" in error_message:
            error_message = "文件生成失败，请重试"
        
        # 返回更友好的错误信息
        raise HTTPException(
            status_code=500,
            detail={
                "message": "生成音频失败",
                "error": error_message
            }
        )

@app.delete("/api/audio/{audio_id}")
async def delete_audio(audio_id: str):
    try:
        file_path = f"static/audio/{audio_id}"
        if os.path.exists(file_path):
            os.remove(file_path)
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 添加获取音频列表的接口
@app.get("/api/audio/{user_id}")
async def list_audio(user_id: str):
    try:
        audio_files = []
        audio_dir = "static/audio"
        for filename in os.listdir(audio_dir):
            if filename.endswith(".mp3") and filename.startswith(f"{user_id}_"):
                file_path = os.path.join(audio_dir, filename)
                file_size = os.path.getsize(file_path)
                try:
                    audio = MP3(file_path)
                    duration = format_duration(audio.info.length)
                except Exception as e:
                    print(f"Error getting duration for {filename}: {str(e)}")
                    duration = "00:00"
                
                audio_files.append({
                    "url": f"/static/audio/{filename}",
                    "name": filename,
                    "size": f"{file_size / 1024:.1f}KB",
                    "duration": duration,
                    "id": filename
                })
        return audio_files
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/subtitle/{audio_id}")
async def get_subtitle(audio_id: str):
    try:
        print(f"Requesting subtitle for audio: {audio_id}")
        
        # 确保文件名格式正确
        base_name = audio_id.replace('.mp3', '')
        subtitle_path = f"static/audio/{base_name}.srt"
        
        print(f"Looking for subtitle file: {subtitle_path}")
        
        # 如果字幕文件不存在，返回404
        if not os.path.exists(subtitle_path):
            print(f"Subtitle file not found: {subtitle_path}")
            raise HTTPException(status_code=404, detail="字幕文件不存在")
        
        # 直接使用 FileResponse，但设置正确的 headers
        return FileResponse(
            path=subtitle_path,
            filename=f"{base_name}.srt",
            headers={
                "Content-Disposition": f'attachment; filename="{base_name}.srt"',
                "Content-Type": "text/srt"
            }
        )
    except Exception as e:
        print(f"Error serving subtitle: {str(e)}")
        if isinstance(e, HTTPException):
            raise
        raise HTTPException(status_code=500, detail=str(e))

# 添加时间格式化辅助函数
def format_time(ms):
    """将毫秒转换为 SRT 时间格式 (HH:MM:SS,mmm)"""
    hours = ms // 3600000
    minutes = (ms % 3600000) // 60000
    seconds = (ms % 60000) // 1000
    milliseconds = ms % 1000
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

# 添加清理函数
async def cleanup_old_files():
    """清理超过30分钟的音频和字幕文件"""
    while True:
        try:
            print("Starting cleanup check...")
            current_time = time.time()
            audio_dir = "static/audio"
            
            # 遍历音频目录
            for filename in os.listdir(audio_dir):
                file_path = os.path.join(audio_dir, filename)
                # 获取文件修改时间
                file_mtime = os.path.getmtime(file_path)
                # 如果文件超过30分钟
                if current_time - file_mtime > 30 * 60:  # 30分钟 = 1800秒
                    try:
                        os.remove(file_path)
                        print(f"Cleaned up old file: {filename}")
                    except Exception as e:
                        print(f"Error deleting file {filename}: {str(e)}")
            
            print("Cleanup check completed")
            
        except Exception as e:
            print(f"Error during cleanup: {str(e)}")
        
        # 等待5分钟后再次检查
        await asyncio.sleep(5 * 60)  # 5分钟 = 300秒

# 修改主函数，启动清理任务
if __name__ == "__main__":
    import uvicorn
    
    # 创建清理任务
    @app.on_event("startup")
    async def startup_event():
        asyncio.create_task(cleanup_old_files())
    
    uvicorn.run(app, host="0.0.0.0", port=8005) 