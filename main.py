import os
import sys
import json
import tkinter as tk
from tkinter import ttk
import pygetwindow as gw
import pyautogui
import threading
import time
import websockets
import asyncio
from loguru import logger

# 创建 GUI 界面
class WindowCaptureApp:
    def __init__(self, root):
        self.stop_flag = True
        # 弹幕数据缓存 用于去重
        self.comment_cache = []
        self.like_cache = []

        self.root = root
        self.root.title("直播数据监听工具-OCR")
        
        # 初始化变量
        self.config_file = 'config.json'
        self.top_left = (0, 0)
        self.bottom_right = (0, 0)

        # 平台下拉框
        self.platform_label = ttk.Label(root, text="选择平台:")
        self.platform_label.grid(row=0, column=0, padx=10, pady=5)
        self.platform_var = tk.StringVar()
        self.platform_list = ['抖音']
        self.platform_dropdown = ttk.Combobox(root, textvariable=self.platform_var, state='readonly', values=self.platform_list, width=50)
        self.platform_dropdown.grid(row=0, column=1, padx=10, pady=5)
        
        # 窗口下拉框
        self.window_label = ttk.Label(root, text="选择窗口:")
        self.window_label.grid(row=1, column=0, padx=10, pady=5)
        self.window_var = tk.StringVar()
        self.window_dropdown = ttk.Combobox(root, textvariable=self.window_var, state='readonly', width=50)
        self.window_dropdown.grid(row=1, column=1, padx=10, pady=5)
        # 刷新按钮
        self.refresh_button = ttk.Button(root, text="刷新窗口列表", command=self.refresh_windows)
        self.refresh_button.grid(row=1, column=2, padx=10, pady=5)

        # 坐标获取按钮和标签
        self.coord_label = ttk.Label(root, text="获取坐标:")
        self.coord_label.grid(row=2, column=0, padx=10, pady=5)

        self.top_left_button = ttk.Button(root, text="获取左上坐标", command=lambda: self.get_mouse_position("top_left"))
        self.top_left_button.grid(row=2, column=1, padx=10, pady=5)

        self.bottom_right_button = ttk.Button(root, text="获取右下坐标", command=lambda: self.get_mouse_position("bottom_right"))
        self.bottom_right_button.grid(row=2, column=2, padx=10, pady=5)

        self.top_left_var = tk.StringVar(value="左上坐标未设置")
        self.bottom_right_var = tk.StringVar(value="右下坐标未设置")

        self.top_left_label = ttk.Label(root, textvariable=self.top_left_var)
        self.top_left_label.grid(row=3, column=1, padx=10, pady=5)

        self.bottom_right_label = ttk.Label(root, textvariable=self.bottom_right_var)
        self.bottom_right_label.grid(row=3, column=2, padx=10, pady=5)

        # 截图延时输入框
        self.ocr_interval_label = ttk.Label(root, text="截图延时S:")
        self.ocr_interval_label.grid(row=4, column=0, padx=10, pady=5)
        self.ocr_interval_var = tk.DoubleVar(value=0.2)
        self.ocr_interval_entry = ttk.Entry(root, textvariable=self.ocr_interval_var, width=50)
        self.ocr_interval_entry.grid(row=4, column=1, padx=10, pady=5)

        # 分数输入框
        self.score_label = ttk.Label(root, text="分数阈值:")
        self.score_label.grid(row=5, column=0, padx=10, pady=5)
        self.score_var = tk.DoubleVar(value=0.2)
        self.score_entry = ttk.Entry(root, textvariable=self.score_var, width=50)
        self.score_entry.grid(row=5, column=1, padx=10, pady=5)

        # 保存按钮
        self.save_button = ttk.Button(root, text="保存配置", command=self.save_config)
        self.save_button.grid(row=6, column=0, padx=10, pady=5)

        # 运行按钮
        self.run_button = ttk.Button(root, text="运行程序", command=self.run_program, width=50)
        self.run_button.grid(row=6, column=1, padx=10, pady=5)

        # 停止按钮
        self.run_button = ttk.Button(root, text="停止程序", command=self.stop_program)
        self.run_button.grid(row=6, column=2, padx=10, pady=5)

        # 加载配置文件
        self.load_config()

        # 初始化窗口列表
        self.refresh_windows()

    def refresh_windows(self):
        """刷新窗口列表"""
        if self.platform == "":
            self.platform_dropdown.current(0)
        else:
            idx = self.platform_list.index(self.platform)
            self.platform_dropdown.current(idx)

        windows = gw.getAllTitles()
        windows = [win for win in windows if win]  # 去除空窗口标题
        self.window_dropdown['values'] = windows
        if windows:
            self.window_dropdown.current(0)
        # 如果配置中有选定的窗口，设置为默认选项
        if self.selected_window_title:
            idx = windows.index(self.selected_window_title) if self.selected_window_title in windows else 0
            self.window_dropdown.current(idx)

    def get_mouse_position(self, position_type):
        """获取鼠标坐标"""
        def wait_and_get_position():
            time.sleep(5)
            x, y = pyautogui.position()
            if position_type == "top_left":
                self.top_left = (x, y)
                self.screen_left = x
                self.screen_top = y
                self.top_left_var.set(f"左上: ({x}, {y})")
            elif position_type == "bottom_right":
                self.screen_right = x
                self.screen_bottom = y
                self.bottom_right = (x, y)
                self.bottom_right_var.set(f"右下: ({x}, {y})")

        # 提示用户并开始倒计时
        threading.Thread(target=wait_and_get_position).start()
        logger.info(f"5秒后获取{position_type}坐标，请将鼠标移到目标位置")

    def load_config(self):
        """从 config.json 文件中加载配置"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config_data = json.load(f)
            self.platform = self.config_data.get('platform', '抖音')
            self.selected_window_title = self.config_data['screen_ocr'].get('selected_window_title', "")
            self.screen_left = self.config_data['screen_ocr'].get('screen_left', 0)
            self.screen_top = self.config_data['screen_ocr'].get('screen_top', 0)
            self.screen_right = self.config_data['screen_ocr'].get('screen_right', 0)
            self.screen_bottom = self.config_data['screen_ocr'].get('screen_bottom', 0)
            self.ocr_interval_var.set(self.config_data['screen_ocr'].get('ocr_interval', 0.5))
            self.score_var.set(self.config_data['screen_ocr'].get('score', 0.2))
            # 显示已加载的坐标
            self.top_left_var.set(f"左上: ({self.screen_left}, {self.screen_top})")
            self.bottom_right_var.set(f"右下: ({self.screen_right}, {self.screen_bottom})")
            logger.info("配置已加载")
        else:
            self.platform = '抖音'
            self.selected_window_title = ""
            logger.error("未找到配置文件，使用默认值")

    def save_config(self):
        """保存配置到 config.json"""
        self.config_data["platform"] = self.platform_var.get()
        self.config_data["screen_ocr"]["selected_window_title"] = self.window_var.get()
        self.config_data["screen_ocr"]["ocr_interval"] = float(self.ocr_interval_var.get())
        self.config_data["screen_ocr"]["score"] = float(self.score_var.get())
        self.config_data["screen_ocr"]["screen_left"] = int(self.screen_left)
        self.config_data["screen_ocr"]["screen_top"] = int(self.screen_top)
        self.config_data["screen_ocr"]["screen_right"] = int(self.screen_right)
        self.config_data["screen_ocr"]["screen_bottom"] = int(self.screen_bottom)
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(self.config_data, f, indent=4, ensure_ascii=False)

        logger.info("配置已保存到 config.json")

    def run_program(self):
        """运行主程序"""
        logger.info("程序已启动...")
        logger.warning("请前置监听窗口，并确保窗口标题与配置文件中的标题一致，不用遮挡或隐藏窗口！")
        logger.warning("若希望监听窗口自动保持前置，请使用 管理员权限运行本程序！")
        # 启动时可以根据需要调用主程序逻辑

        if self.stop_flag:
            self.stop_flag = False

            # 单独启动一个线程来运行主程序，避免阻塞主线程
            threading.Thread(target=self.loop_screen_ocr).start()

    def stop_program(self):
        """停止程序"""
        self.stop_flag = True

    def loop_screen_ocr(self):
        # 尝试获取选择的窗口
        try:
            from cnocr import CnOcr

            # 使用 OCR 识别 首次使用时会下载模型
            ocr = CnOcr()  # 所有参数都使用默认值
        
            while True:
                # 判断是否被停止运行
                if self.stop_flag:
                    logger.info("程序已停止")
                    break

                selected_window_title = self.window_var.get()
                window = gw.getWindowsWithTitle(selected_window_title)[0]

                try:
                    # 确保窗口未最小化并将其激活
                    if window.isMinimized:
                        window.restore()  # 恢复窗口

                    # 激活窗口
                    window.activate()  # 激活窗口

                except IndexError:
                    logger.error("所选窗口不存在或无法找到。")
                except gw.PyGetWindowException as e:
                    logger.debug(f"激活窗口时出错: {e}")

                # 等待一小段时间以确保窗口被激活（可选）
                # pyautogui.sleep(0.5)

                # 输出窗口的位置、大小
                logger.debug(f"窗口位置 左上、右下: ({window.left}, {window.top})， ({window.right}, {window.bottom})")
                logger.debug(f"窗口宽高: ({window.width}, {window.height})")

                # 获取窗口位置和大小
                left, top = int(self.screen_left), int(self.screen_top)
                width, height = abs(int(self.screen_right) - int(self.screen_left)), abs(int(self.screen_bottom) - int(self.screen_top))

                # 使用 pyautogui 截取屏幕图像
                screenshot = pyautogui.screenshot(region=(left, top, width, height))

                # 保存图像到本地
                screenshot.save('captured_image_pyautogui.png')  # 保存为 PNG 格式

                # 区分平台，因为平台不一样 解析规则不一样 图片结构不一样
                if self.platform == '抖音':
                    def is_valid_comment(s):
                        import re 

                        # 定义正则表达式模式
                        pattern = r'^.{1,}：.{1,}$'
                        
                        # 使用 re.match 来检查字符串是否匹配模式
                        if re.match(pattern, s):
                            return True
                        else:
                            return False
                        
                    def contains_any_line_from_file(target_string, file_path):
                        # 判断文件是否存在
                        if not os.path.exists(file_path):
                            return False

                        # 打开文件并逐行读取
                        with open(file_path, 'r', encoding='utf-8') as file:
                            for line in file:
                                # 去掉每行末尾的换行符
                                line = line.strip()
                                # 检查目标字符串是否包含该行
                                if line in target_string:
                                    return True
                        # 如果没有找到匹配的行，返回 False
                        return False

                    
                    ret_json = ocr.ocr(screenshot)
                    for data in ret_json:
                        # 识别分数低于 0.2 的结果会被忽略
                        if data["score"] > 0.2:
                            # logger.info(f"获取的内容:{data['text']}")
                            # 仅保留 形如  xx：xx 长度不限的结果
                            if is_valid_comment(data['text']):
                                username = data['text'].split('：')[0]
                                comment = data['text'].split('：')[1]

                                # 判断是否为点赞消息
                                if '为主播点赞了' == comment:
                                    # 创建唯一标识符用于去重（比如"用户名+弹幕内容"的组合）
                                    unique_like = f"{username}:{comment}"

                                    # 如果弹幕已经存在于缓存中则跳过发送
                                    if unique_like in self.like_cache:
                                        continue

                                    # 如果是新的弹幕，将其加入缓存并发送
                                    self.like_cache.append(unique_like)

                                    if len(self.like_cache) > int(self.config_data["screen_ocr"]["max_cache"]["like"]):  # 假设缓存最大容量为 50
                                        # 删除最旧的弹幕
                                        self.like_cache.pop()

                                    logger.info(f"[点赞消息] {username}：{comment}")

                                    data_json = {
                                        "type": "like",
                                        "username": username,
                                        "comment": comment
                                    }

                                    # 使用 asyncio 来发送消息
                                    asyncio.run(broadcast_to_clients(json.dumps(data_json, ensure_ascii=False)))

                                    continue

                                # 过滤礼物数据
                                if '送出了' in comment:
                                    logger.debug(f"[礼物消息] {username}：{comment}")
                                    continue

                                # 违禁词过滤
                                if contains_any_line_from_file(comment, "data/违禁词.txt"):
                                    continue

                                # 创建唯一标识符用于去重（比如"用户名+弹幕内容"的组合）
                                unique_comment = f"{username}:{comment}"

                                # 如果弹幕已经存在于缓存中则跳过发送
                                if unique_comment in self.comment_cache:
                                    # logger.debug(f"重复弹幕: {unique_comment}")
                                    continue

                                # 如果是新的弹幕，将其加入缓存并发送
                                self.comment_cache.append(unique_comment)

                                if len(self.comment_cache) > int(self.config_data["screen_ocr"]["max_cache"]["comment"]):  # 假设缓存最大容量为 50
                                    # 删除最旧的弹幕
                                    self.comment_cache.pop(0)
                                
                                logger.info(f"[弹幕消息] {username}：{comment}")

                                data_json = {
                                    "type": "comment",
                                    "username": username,
                                    "comment": comment
                                }

                                # 使用 asyncio 来发送消息
                                asyncio.run(broadcast_to_clients(json.dumps(data_json, ensure_ascii=False)))

                # 识别间隔
                time.sleep(float(self.ocr_interval_var.get()))
        except Exception as e:
            logger.error(f"发生错误: {e}")


# 配置 logger
def configure_logger(file_path, log_level, max_file_size):
    level = log_level.upper() if log_level else "INFO"
    max_size = max_file_size if max_file_size else "1024 MB"

    # 清空之前的handlers
    logger.remove()

    # 配置控制台输出
    # logger.add(sys.stderr, format="{time:YYYY-MM-DD HH:mm:ss.SSS} | <lvl>{level:8}</>| <lvl>{message}</>", colorize=True, level=level)
    logger.add(sys.stderr, colorize=True, level=level)

    # 配置文件输出
    logger.add(file_path, level=level, rotation=max_size)


async def websocket_handler(websocket, path):
    # 添加客户端
    ws_clients.add(websocket)
    try:
        async for message in websocket:
            pass  # 可以根据需要处理来自客户端的消息
    except websockets.exceptions.ConnectionClosedOK:
        pass
    finally:
        # 移除客户端
        ws_clients.remove(websocket)

def start_websocket_server(ip, port):
    logger.info(f"WebSocket服务器启动，监听地址：{ip}:{port}")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    start_server = websockets.serve(websocket_handler, ip, port)
    loop.run_until_complete(start_server)
    loop.run_forever()

async def broadcast_to_clients(message):
    if ws_clients:
        await asyncio.wait([client.send(message) for client in ws_clients])

# 启动 GUI 应用
if __name__ == "__main__":
    try:
        ws_clients = set()

        config_file = "config.json"
        with open(config_file, 'r', encoding='utf-8') as f:
            config_data = json.load(f)

        # 获取日志配置
        log_level = config_data["loguru"].get("level", "INFO")
        max_file_size = config_data["loguru"].get("max_file_size", "1024 MB")

        # 配置 logger
        configure_logger("log.txt", log_level, max_file_size)

        ws_ip = str(config_data["ws"]["ip"])
        ws_port = int(config_data["ws"]["port"])

        threading.Thread(target=start_websocket_server, args=[ws_ip, ws_port], daemon=True).start()

        root = tk.Tk()
        app = WindowCaptureApp(root)
        root.mainloop()
    except Exception as e:
        print(f"An error occurred: {e}")
        input("Press Enter to exit...")
