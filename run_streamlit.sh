#!/bin/bash

# 线条动画生成器 - Streamlit快速启动脚本

echo "准备启动Apple风格文字动画生成器..."

# 检查是否安装了pip
if ! command -v pip3 &> /dev/null; then
    echo "错误: 未找到pip3，请先安装Python和pip"
    exit 1
fi

# 检查streamlit_app.py是否存在
if [ ! -f "streamlit_app.py" ]; then
    echo "错误: 未找到streamlit_app.py文件"
    echo "当前目录文件列表:"
    ls -la
    exit 1
fi

# 检查是否安装了streamlit
if ! python3 -c "import streamlit" &> /dev/null; then
    echo "正在安装Streamlit和依赖项..."
    pip3 install -r streamlit_requirements.txt
fi

# 确保上传目录存在
mkdir -p static/uploads

# 使用不同的端口
PORT=8888

echo "启动Streamlit应用..."
echo "应用启动后，将自动在浏览器中打开"
echo "您也可以通过以下地址访问：http://localhost:$PORT"
echo "按Ctrl+C可以停止应用"
echo "-----------------------------------"

# 启动Streamlit应用，尝试使用localhost而不是0.0.0.0
python3 -m streamlit run streamlit_app.py --server.address=localhost --server.port=$PORT