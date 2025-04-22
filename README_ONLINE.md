# 线条动画生成器 - 在线使用指南

这个指南将帮助您快速设置线条动画生成器，让用户可以直接通过网络连接预览和生成线条视频，无需复杂部署。

## 快速开始

我们提供了多种方式让您的线条动画生成器可以在线访问：

### 方式一：使用Streamlit（最简单）

1. 在终端中运行以下命令：
   ```
   ./run_streamlit.sh
   ```
   或者手动执行：
   ```
   pip install -r streamlit_requirements.txt
   streamlit run streamlit_app.py
   ```

2. 应用将自动在浏览器中打开，默认地址为：http://localhost:8501

3. 要让其他人通过网络访问，您可以使用以下命令：
   ```
   streamlit run streamlit_app.py --server.address=0.0.0.0
   ```
   然后其他人可以通过 http://您的IP地址:8501 访问

### 方式二：使用Streamlit Cloud（免费托管）

1. 将代码推送到GitHub仓库

2. 访问 [Streamlit Cloud](https://streamlit.io/cloud) 并注册账户

3. 连接您的GitHub仓库并部署应用

4. 获取公共URL并分享给用户

### 方式三：使用PythonAnywhere（免费托管）

详细步骤请参考 `QUICK_START.md` 文件中的PythonAnywhere部署指南。

## 使用说明

无论使用哪种方式部署，用户都可以通过浏览器访问应用，并：

1. 输入想要的文字
2. 选择字体和大小
3. 预览效果
4. 生成并下载视频

## 优势

- **无需安装**：用户只需一个浏览器即可使用
- **随时访问**：通过URL可以随时随地访问
- **易于分享**：只需分享链接即可让他人使用
- **跨平台**：支持所有现代浏览器和设备

## 注意事项

- 视频生成可能需要一些时间，特别是在免费托管服务上
- 对于高流量使用，建议升级到付费托管服务
- 确保您的服务器有足够的资源处理视频生成

## 技术支持

如有问题，请参考 `QUICK_START.md` 获取更多详细信息。