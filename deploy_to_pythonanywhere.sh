#!/bin/bash

# 这是一个简单的部署脚本，帮助将应用部署到PythonAnywhere
# 注意：你需要先在PythonAnywhere上创建账户

echo "准备部署Apple风格文字动画生成器到PythonAnywhere..."

# 确保依赖已安装
pip install -r requirements.txt

# 创建必要的目录
mkdir -p static/uploads
chmod 777 static/uploads

echo "请按照以下步骤完成部署："
echo "1. 登录到你的PythonAnywhere账户"
echo "2. 上传所有项目文件到PythonAnywhere"
echo "3. 在Web选项卡中创建一个新的Web应用"
echo "4. 选择Flask框架，并将WSGI配置文件指向wsgi.py"
echo "5. 在控制台中运行：pip install ffmpeg-python"
echo "6. 重启Web应用"

echo "完成上述步骤后，你的应用将可以通过你的PythonAnywhere URL访问"
echo "例如：http://yourusername.pythonanywhere.com"