# 线条动画生成器快速启动指南

这个指南将帮助您快速启动线条动画生成器，无需复杂的部署过程，让用户可以直接通过网络连接预览和生成线条视频。

## 方案一：使用PythonAnywhere（推荐新手）

PythonAnywhere是一个基于云的Python开发和托管环境，可以免费托管您的应用。

### 步骤：

1. 注册[PythonAnywhere](https://www.pythonanywhere.com/)账户（免费版即可）

2. 登录后，进入Dashboard，点击"Files"标签，上传项目文件
   - 您可以使用"Upload a file"功能上传单个文件
   - 或者使用Bash控制台，通过git克隆整个项目

3. 在Dashboard中，点击"Web"标签，然后点击"Add a new web app"

4. 选择"Flask"框架，并将WSGI配置文件指向`wsgi.py`

5. 在"Consoles"标签中打开一个Bash控制台，运行以下命令安装依赖：
   ```
   pip3 install --user -r requirements.txt
   ```

6. 回到"Web"标签，点击"Reload"按钮重启应用

7. 现在您可以通过分配的URL访问应用，格式为：`http://您的用户名.pythonanywhere.com`

## 方案二：使用Streamlit分享（最简单）

如果您想要更简单的方法，可以使用Streamlit，它提供了一个简单的方式来创建和分享数据应用。

### 步骤：

1. 安装Streamlit：
   ```
   pip install streamlit
   ```

2. 创建一个新的`streamlit_app.py`文件，将现有的Flask应用转换为Streamlit应用

3. 注册[Streamlit Sharing](https://streamlit.io/sharing)账户

4. 将代码推送到GitHub仓库

5. 在Streamlit Sharing中部署您的应用

6. 分享生成的URL给用户

## 方案三：本地运行并使用ngrok暴露服务（开发测试用）

如果您只是想临时分享给他人使用，可以在本地运行应用并使用ngrok创建一个公共URL。

### 步骤：

1. 安装依赖：
   ```
   pip install -r requirements.txt
   ```

2. 运行Flask应用：
   ```
   python app.py
   ```

3. 安装并设置ngrok：
   - 从[ngrok官网](https://ngrok.com/)下载并安装
   - 注册账户并获取认证令牌
   - 运行命令：`ngrok http 8000`

4. ngrok将提供一个公共URL（如`https://xxxx.ngrok.io`），您可以分享给任何人

## 方案四：使用Heroku（适合长期使用）

项目已包含Procfile，可以直接部署到Heroku。

### 步骤：

1. 注册[Heroku](https://www.heroku.com/)账户

2. 安装[Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)

3. 登录Heroku：
   ```
   heroku login
   ```

4. 创建Heroku应用：
   ```
   heroku create 您的应用名称
   ```

5. 部署应用：
   ```
   git push heroku main
   ```

6. 打开应用：
   ```
   heroku open
   ```

## 注意事项

- 所有方案都提供了一个URL，用户可以直接通过浏览器访问
- 用户无需安装任何软件，只需一个现代浏览器
- 视频生成可能需要一些时间，特别是在免费托管服务上
- 对于生产环境，建议使用付费服务以获得更好的性能和可靠性