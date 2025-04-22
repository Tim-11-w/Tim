import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patheffects as path_effects
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties
from matplotlib.transforms import Affine2D
import moviepy.editor as mpy
import os
import tkinter as tk
from tkinter import ttk, font
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AppleTextAnimation:
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
        
        # 使用moviepy保存为视频
        plt.close(self.fig)  # 避免显示图形
        
        # 创建临时GIF文件
        temp_gif = "temp_animation.gif"
        anim.save(temp_gif, writer='pillow', fps=self.fps, dpi=100)
        
        # 转换为MP4
        clip = mpy.VideoFileClip(temp_gif)
        clip.write_videofile(output_path, fps=self.fps)
        
        # 删除临时文件
        os.remove(temp_gif)
        
        return output_path
    
    def preview_animation(self):
        """预览动画"""
        anim = self.create_animation()
        plt.show()
        
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


class AnimationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Apple风格文字动画生成器")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")
        
        self.animator = AppleTextAnimation()
        
        self.create_widgets()
        
    def create_widgets(self):
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 控制面板
        control_frame = ttk.LabelFrame(main_frame, text="控制面板", padding="10")
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        # 文本输入
        ttk.Label(control_frame, text="输入文字:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.text_var = tk.StringVar(value="Hello")
        ttk.Entry(control_frame, textvariable=self.text_var, width=20).grid(row=0, column=1, pady=5)
        
        # 字体选择
        ttk.Label(control_frame, text="选择字体:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.font_var = tk.StringVar(value="Arial")
        font_list = list(font.families())
        font_combo = ttk.Combobox(control_frame, textvariable=self.font_var, values=font_list, width=18)
        font_combo.grid(row=1, column=1, pady=5)
        
        # 字体大小
        ttk.Label(control_frame, text="字体大小:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.size_var = tk.IntVar(value=72)
        ttk.Spinbox(control_frame, from_=10, to=200, textvariable=self.size_var, width=5).grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # 动画持续时间
        ttk.Label(control_frame, text="动画时长(秒):").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.duration_var = tk.DoubleVar(value=5.0)
        ttk.Spinbox(control_frame, from_=1, to=20, increment=0.5, textvariable=self.duration_var, width=5).grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # 按钮
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="预览", command=self.preview).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="保存视频", command=self.save_video).pack(side=tk.LEFT, padx=5)
        
        # 预览区域
        preview_frame = ttk.LabelFrame(main_frame, text="预览", padding="10")
        preview_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建matplotlib图形用于预览
        self.preview_fig, self.preview_ax = plt.subplots(figsize=(8, 5), facecolor='black')
        self.preview_ax.set_facecolor('black')
        self.preview_ax.set_xlim(0, 10)
        self.preview_ax.set_ylim(0, 6)
        self.preview_ax.axis('off')
        
        # 将matplotlib图形嵌入到tkinter中
        self.canvas = FigureCanvasTkAgg(self.preview_fig, master=preview_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # 状态栏
        self.status_var = tk.StringVar(value="就绪")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def update_preview(self):
        """更新预览图像"""
        self.preview_ax.clear()
        self.preview_ax.set_facecolor('black')
        self.preview_ax.set_xlim(0, 10)
        self.preview_ax.set_ylim(0, 6)
        self.preview_ax.axis('off')
        
        # 获取当前设置
        text = self.text_var.get()
        font_name = self.font_var.get()
        font_size = self.size_var.get()
        
        # 创建文本路径
        font_prop = FontProperties(family=font_name, size=font_size)
        text_path = TextPath((0, 0), text, prop=font_prop)
        
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
                self.preview_ax.plot(x, y, color='white', lw=2)
        
        self.canvas.draw()
    
    def preview(self):
        """预览动画"""
        # 更新动画器设置
        self.animator.set_text(self.text_var.get())
        self.animator.set_font(self.font_var.get(), self.size_var.get())
        self.animator.set_duration(self.duration_var.get())
        
        # 显示动画预览
        self.status_var.set("正在生成预览...")
        self.root.update()
        self.animator.preview_animation()
        self.status_var.set("就绪")
    
    def save_video(self):
        """保存动画为视频"""
        # 更新动画器设置
        self.animator.set_text(self.text_var.get())
        self.animator.set_font(self.font_var.get(), self.size_var.get())
        self.animator.set_duration(self.duration_var.get())
        
        # 保存视频
        self.status_var.set("正在生成视频...")
        self.root.update()
        output_path = self.animator.save_animation()
        self.status_var.set(f"视频已保存至: {output_path}")


def main():
    root = tk.Tk()
    app = AnimationApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()