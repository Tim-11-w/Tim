import streamlit as st
import os
import base64
import uuid
from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties
from matplotlib.transforms import Affine2D
import matplotlib.font_manager as fm
import tempfile
import time

# 设置页面配置
st.set_page_config(
    page_title="文字动画生成器",
    page_icon="🎬",
    layout="wide"
)

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
    
    def save_animation(self, output_path="text_animation.mp4"):
        """保存动画为视频文件"""
        anim = self.create_animation()
        
        # 使用FFMpegWriter保存为视频
        writer = animation.FFMpegWriter(fps=self.fps, metadata=dict(artist='Me'), bitrate=1800)
        anim.save(output_path, writer=writer)
        plt.close(self.fig)  # 避免显示图形
        
        return output_path
    
    def generate_preview_image(self):
        """生成预览图像"""
        self.text_to_paths()
        
        # 显示所有路径
        for j, path in enumerate(self.paths):
            self.lines[j].set_data(path[:, 0], path[:, 1])
        
        # 将图形保存到内存中的BytesIO对象
        buf = BytesIO()
        self.fig.savefig(buf, format='png', facecolor='black')
        buf.seek(0)
        plt.close(self.fig)  # 避免显示图形
        
        return buf

# 获取系统字体列表
def get_system_fonts():
    fonts = [f.name for f in fm.fontManager.ttflist]
    # 去重并排序
    fonts = sorted(list(set(fonts)))
    return fonts

# 主应用界面
st.title("文字动画生成器")
st.markdown("### 创建优雅的文字描边动画")

# 创建两列布局
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("控制面板")
    
    # 输入文字
    text_input = st.text_input("输入文字", value="Hello")
    
    # 选择字体
    fonts = get_system_fonts()
    font_select = st.selectbox("选择字体", fonts, index=fonts.index("Arial") if "Arial" in fonts else 0)
    
    # 字体大小
    size_input = st.slider("字体大小", min_value=10, max_value=200, value=72)
    
    # 动画时长
    duration_input = st.slider("动画时长(秒)", min_value=1.0, max_value=20.0, value=5.0, step=0.5)

with col2:
    st.subheader("预览")
    preview_container = st.empty()
    
    # 预览按钮
    if st.button("预览"):
        with st.spinner("正在生成预览..."):
            try:
                # 创建动画对象
                animation = AppleTextAnimation()
                animation.text = text_input
                animation.font_name = font_select
                animation.font_size = size_input
                
                # 生成预览图像
                preview_image = animation.generate_preview_image()
                preview_container.image(preview_image, caption="预览图像", use_column_width=True)
                st.success("预览生成完成")
            except Exception as e:
                st.error(f"预览生成失败: {str(e)}")
    
    # 生成视频按钮
    if st.button("生成视频"):
        with st.spinner("正在生成视频，这可能需要一些时间..."):
            try:
                # 创建临时文件
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
                temp_file.close()
                output_path = temp_file.name
                
                # 创建动画对象
                animation = AppleTextAnimation()
                animation.text = text_input
                animation.font_name = font_select
                animation.font_size = size_input
                animation.duration = duration_input
                animation.frames = int(animation.duration * animation.fps)
                
                # 生成视频
                animation.save_animation(output_path)
                
                # 显示视频
                with open(output_path, "rb") as file:
                    video_bytes = file.read()
                
                st.video(video_bytes)
                
                # 提供下载链接
                st.download_button(
                    label="下载视频",
                    data=video_bytes,
                    file_name=f"text_animation_{text_input}.mp4",
                    mime="video/mp4"
                )
                
                st.success("视频生成完成")
                
                # 清理临时文件
                try:
                    os.unlink(output_path)
                except:
                    pass
                    
            except Exception as e:
                st.error(f"视频生成失败: {str(e)}")

# 添加使用说明
st.markdown("---")
st.markdown("### 使用说明")
st.markdown("""
1. 在左侧控制面板输入您想要的文字
2. 选择合适的字体和大小
3. 点击"预览"按钮查看效果
4. 调整动画时长
5. 点击"生成视频"按钮创建完整动画
6. 下载生成的视频文件
""")

# 添加页脚
st.markdown("---")
st.markdown("© 2023 Apple风格文字动画生成器 | 无需部署，直接使用")
