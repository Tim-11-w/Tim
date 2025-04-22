# 文字动画生成器

一个可以生成线条文字动画的Web应用，支持自定义文本、字体和动画时长。

## 功能特点

- 生成文字描边动画
- 支持自定义文本内容
- 可选择多种字体
- 可调整字体大小
- 可设置动画时长
- 提供实时预览功能
- 支持视频下载

## 安装依赖

在运行程序前，请确保安装以下Python库：

```bash
pip install -r requirements.txt
```

同时，确保系统已安装FFmpeg：

- **Windows**: 下载FFmpeg并添加到系统PATH
- **macOS**: `brew install ffmpeg`
- **Linux**: `sudo apt-get install ffmpeg`

## 本地运行

1. 克隆仓库到本地
2. 安装依赖
3. 运行Flask应用：

```bash
python app.py
```

4. 在浏览器中访问 `http://localhost:8000`

## 部署为公开网页

要将此应用部署为公开网页，让所有人都可以通过链接使用，请参考 [DEPLOYMENT.md](DEPLOYMENT.md) 文件中的详细部署指南。

### 快速部署选项

- **PythonAnywhere**: 适合新手，使用 `deploy_to_pythonanywhere.sh` 脚本辅助部署
- **Heroku**: 使用提供的 `Procfile` 快速部署
- **AWS Elastic Beanstalk**: 使用 `.ebextensions` 配置自动安装依赖

## 使用方法

1. 在输入框中输入想要动画的文字
2. 选择合适的字体和大小
3. 设置动画时长
4. 点击"预览"按钮查看效果
5. 满意后点击"生成视频"按钮
6. 等待视频生成完成后，可以在线观看或下载

## 技术实现

- 前端：HTML, CSS, JavaScript, Bootstrap
- 后端：Flask
- 动画生成：Matplotlib, MoviePy
- 视频处理：FFmpeg

## 许可证

MIT