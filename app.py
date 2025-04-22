import os
import base64
import uuid
from io import BytesIO
from flask import Flask, render_template, request, jsonify, send_file, url_for
from flask_cors import CORS
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties
from matplotlib.transforms import Affine2D

# 获取环境变量或使用默认值
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
PORT = int(os.environ.get('PORT', 8000))

app = Flask(__name__)
# 启用CORS，允许所有来源的跨域请求
CORS(app)

# 确保上传和临时文件夹存在
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class TextAnimation:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(10, 6), facecolor='black')
        self.ax.set_facecolor('black')
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 6)
        self.ax.axis('off')
        
        # 动画参数
        self.text = "Hello"
        self.font_name = "Arial"
        self.font_size = 72
        self.line_color = 'white'
        self.duration = 5  # 动画持续时间（秒）
        self.fps = 30      # 帧率
        self.frames = self.duration * self.fps
        self.line_width = 2
        
        # 路径点和动画状态
        self.paths = []
        self.points = []
        self.lines = []
        
    def text_to_paths(self):
        """将文本转换为路径点"""
        font_prop = FontProperties(family=self.font_name, size=self.font_size)
        text_path = TextPath((0, 0), self.text, prop=font_prop)
        
        # 获取文本边界以便居中
        text_bounds = text_path.get_extents()
        width = text_bounds.width
        height = text_bounds.height
        
        # 创建变换以居中文本
        transform = Affine2D().translate(5 - width/2, 3 - height/2)
        text_path = transform.transform_path(text_path)
        
        # 提取路径点
        self.paths = []
        for path in text_path.to_polygons():
            if len(path) > 2:  # 确保路径至少有3个点
                self.paths.append(path)
        
        # 为每个路径创建点和线条
        self.points = [np.zeros((1, 2)) for _ in self.paths]
        self.lines = [self.ax.plot([], [], color=self.line_color, lw=self.line_width)[0] 
                     for _ in self.paths]
    
    def init_animation(self):
        """初始化动画"""
        for line in self.lines:
            line.set_data([], [])
        return self.lines
    
    def animate(self, i):
        """更新每一帧的动画"""
        progress = i / self.frames
        
        for j, path in enumerate(self.paths):
            # 计算当前应该显示的点数
            path_progress = min(1.0, max(0, (progress * 1.5) - (j * 0.05)))
            if path_progress <= 0:
                continue
                
            points_to_show = int(path_progress * len(path))
            if points_to_show > 0:
                self.points[j] = path[:points_to_show]
                self.lines[j].set_data(self.points[j][:, 0], self.points[j][:, 1])
        
        return self.lines
    
    def create_animation(self):
        """创建动画对象"""
        self.text_to_paths()
        anim = animation.FuncAnimation(self.fig, self.animate, frames=self.frames,
                                      init_func=self.init_animation, blit=True)
        return anim
    
    def save_animation(self, output_path="apple_text_animation.mp4"):
        """保存动画为视频文件"""
        anim = self.create_animation()
        
        # 直接使用matplotlib保存为MP4
        plt.close(self.fig)  # 避免显示图形
        
        # 使用FFMpegWriter保存为MP4
        writer = animation.FFMpegWriter(fps=self.fps, metadata=dict(artist='Me'), bitrate=1800)
        anim.save(output_path, writer=writer)
        
        return output_path
    
    def generate_preview_image(self):
        """生成预览图像"""
        # 清除当前图形
        self.ax.clear()
        self.ax.set_facecolor('black')
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 6)
        self.ax.axis('off')
        
        # 创建文本路径
        font_prop = FontProperties(family=self.font_name, size=self.font_size)
        text_path = TextPath((0, 0), self.text, prop=font_prop)
        
        # 获取文本边界以便居中
        text_bounds = text_path.get_extents()
        width = text_bounds.width
        height = text_bounds.height
        
        # 创建变换以居中文本
        transform = Affine2D().translate(5 - width/2, 3 - height/2)
        text_path = transform.transform_path(text_path)
        
        # 绘制文本轮廓
        for path in text_path.to_polygons():
            if len(path) > 2:
                x, y = path[:, 0], path[:, 1]
                self.ax.plot(x, y, color='white', lw=2)
        
        # 将图形转换为base64编码的图像
        buffer = BytesIO()
        self.fig.savefig(buffer, format='png', facecolor='black')
        buffer.seek(0)
        image_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        return image_data
        
    def set_text(self, text):
        """设置要动画的文本"""
        self.text = text
        
    def set_font(self, font_name, font_size):
        """设置字体和大小"""
        self.font_name = font_name
        self.font_size = font_size
        
    def set_duration(self, duration):
        """设置动画持续时间"""
        self.duration = duration
        self.frames = self.duration * self.fps

@app.route('/')
def index():
    return render_template('index.html', title="文字动画生成器")

@app.route('/preview', methods=['POST'])
def preview():
    # 获取表单数据
    text = request.form.get('text', 'Hello')
    font_name = request.form.get('font', 'Arial')
    font_size = int(request.form.get('size', 72))
    
    # 创建动画对象并设置参数
    animator = TextAnimation()
    animator.set_text(text)
    animator.set_font(font_name, font_size)
    
    # 生成预览图像
    preview_image = animator.generate_preview_image()
    
    return jsonify({'preview_image': preview_image})

@app.route('/generate', methods=['POST'])
def generate():
    try:
        # 获取表单数据
        text = request.form.get('text', 'Hello')
        font_name = request.form.get('font', 'Arial')
        font_size = int(request.form.get('size', 72))
        duration = float(request.form.get('duration', 5.0))
        
        # 创建动画对象并设置参数
        animator = TextAnimation()
        animator.set_text(text)
        animator.set_font(font_name, font_size)
        animator.set_duration(duration)
        
        # 生成唯一文件名
        filename = f"animation_{uuid.uuid4().hex}.mp4"
        output_path = os.path.join(UPLOAD_FOLDER, filename)
        
        # 确保上传目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # 保存动画
        try:
            animator.save_animation(output_path)
        except Exception as e:
            # 检查是否是FFmpeg相关错误
            if 'ffmpeg' in str(e).lower():
                return jsonify({'error': 'FFmpeg未安装或不可用。请安装FFmpeg后再试。'}), 500
            raise
        
        # 返回视频文件URL
        video_url = url_for('static', filename=f'uploads/{filename}')
        return jsonify({'video_url': video_url})
    except Exception as e:
        app.logger.error(f"视频生成错误: {str(e)}")
        return jsonify({'error': f"视频生成失败: {str(e)}"}), 500

@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join(UPLOAD_FOLDER, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=DEBUG)