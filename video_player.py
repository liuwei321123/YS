import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
from urllib.parse import quote
import urllib.request
import socket
import threading

class VideoPlayer:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('视频解析播放器')
        self.window.geometry('600x400')
        
        # 使用字典存储接口名称和URL的对应关系
        self.parse_apis = {
            '解析接口1': 'https://jx.m3u8.tv/jiexi/?url=',
            '解析接口2': 'https://jx.aidouer.net/?url=',
            '解析接口3': 'https://jx.playerjy.com/?url=',
            '解析接口4': 'https://jx.jsonplayer.com/player/?url=',
            '解析接口5': 'https://jx.xmflv.com/?url=',
            '解析接口6': 'https://jx.bozrc.com:4433/player/?url=',
            '解析接口7': 'https://jx.777jiexi.com/player/?url=',
            '解析接口8': 'https://api.jiexi.la/?url=',
            '解析接口9': 'https://www.8090g.cn/?url='
        }
        
        self.working_apis = {}  # 存储可用的接口
        self.setup_ui()
        self.check_apis()
    
    def setup_ui(self):
        # 创建说明标签
        label = tk.Label(self.window, text='请输入需要解析的视频链接：', font=('Arial', 12))
        label.pack(pady=20)
        
        # 创建输入框
        self.url_entry = tk.Entry(self.window, width=50)
        self.url_entry.pack(pady=10)
        
        # 创建解析接口下拉框
        self.api_combo = ttk.Combobox(self.window, values=list(self.parse_apis.keys()), width=47)
        self.api_combo.set(list(self.parse_apis.keys())[0])  # 设置默认值
        self.api_combo.pack(pady=10)
        
        # 创建播放按钮
        play_button = tk.Button(self.window, text='播放', command=self.play_video, 
                              width=20, height=2)
        play_button.pack(pady=20)
        
        # 创建说明文本
        tips = tk.Label(self.window, text='支持：爱奇艺、腾讯视频、优酷、芒果TV等主流视频网站',
                       font=('Arial', 10))
        tips.pack(pady=10)
        
        # 添加刷新按钮
        refresh_button = tk.Button(self.window, text='刷新接口', command=self.check_apis,
                                 width=10, height=1)
        refresh_button.pack(pady=5)
        
        # 添加状态标签
        self.status_label = tk.Label(self.window, text='正在检测接口...', font=('Arial', 9))
        self.status_label.pack(pady=5)
        
    def check_apis(self):
        """检测接口可用性"""
        self.status_label.config(text='正在检测接口...')
        self.working_apis = {}
        
        def check():
            socket.setdefaulttimeout(3)
            for name, url in self.parse_apis.items():
                try:
                    test_url = url + quote('https://v.qq.com/x/cover/mzc00200f995x6t.html')
                    response = urllib.request.urlopen(test_url)
                    if response.getcode() == 200:
                        self.working_apis[name] = url
                except:
                    continue
                
            self.window.after(0, self.update_api_list)
        
        threading.Thread(target=check, daemon=True).start()
    
    def update_api_list(self):
        """更新接口列表"""
        if self.working_apis:
            api_names = list(self.working_apis.keys())
            self.api_combo['values'] = api_names
            self.api_combo.set(api_names[0])
            self.status_label.config(text=f'可用接口: {len(self.working_apis)} 个')
        else:
            self.status_label.config(text='警告：没有可用接口')
    
    def play_video(self):
        video_url = self.url_entry.get().strip()
        if not video_url:
            messagebox.showwarning('警告', '请输入视频链接！')
            return
        
        if not self.working_apis:
            messagebox.showwarning('警告', '当前没有可用的解析接口！')
            return
            
        selected_name = self.api_combo.get()
        selected_api = self.working_apis[selected_name]
        parse_url = selected_api + quote(video_url)
        webbrowser.open(parse_url)

if __name__ == '__main__':
    player = VideoPlayer()
    player.window.mainloop() 
