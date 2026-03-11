"""
操纵电脑文件的工具：
1. open_dir：打开文件夹，文件夹不存在则自动创建
2. open_video：打开视频文件
"""

import os
import subprocess
from langchain.tools import tool
from .schema.file_schema import FileSchema

# 打开文件夹的工具
@tool("open_dir", args_schema=FileSchema)
def open_dir(path: str) -> str:
    """
    根据输入的文件夹路径打开文件夹，如果文件夹不存在则自动创建
    支持嵌套路径结构（如 D:\test\test_agent）和完整 URI
    """
    try:
        # 规范化路径（处理反斜杠、空格等）
        normalized_path = os.path.normpath(path)
        
        # 如果文件夹不存在，则创建
        if not os.path.exists(normalized_path):
            os.makedirs(normalized_path, exist_ok=True)
        
        # 使用 subprocess 打开文件夹
        subprocess.Popen(["explorer", normalized_path])
        return f"已打开文件夹：{normalized_path}"
    except Exception as e:
        return f"打开文件夹失败：{e}"
    
# 打开视频的工具
@tool("open_video", args_schema=FileSchema)
def open_video(path: str) -> str:
    """
    根据输入的视频文件路径打开视频文件，如果视频文件不存在则报错
    """
    try:
        # 如果视频文件不存在，则报错
        if not os.path.exists(path):
            return f"视频文件不存在：{path}"
        #  检测文件类型
        if os.path.splitext(path)[1] not in [".mp4", ".avi", ".mkv"]:
            return f"不支持的视频格式：{path}"
        # 打开视频文件
        os.startfile(path)
        return f"已打开视频文件：{path}"
    except Exception as e:
        return f"打开视频文件失败：{e}"
    