<div align="center">

# ✨ OCR数据监听  ✨

</div>

# 前言

基于tkinter开发，使用pyautogui进行屏幕截图，使用CnOCR进行文本识别，最后通过websocket，将解析后的数据发送给所有连接的客户端。

# 环境

python: 3.10  

# 安装

安装依赖：`pip install -r requirements.txt`  

# 运行

补充  
ws连接地址：ws://127.0.0.1:8765  

## 抖音

浏览器打开你想要监听的直播间，按下F12，打开开发者工具，切换到Console，输入以下代码，删除直播画面，延长弹幕框，从而减少换行导致的数据丢失问题：
```
document.getElementsByClassName("__playerIsFull")[0].remove();
document.getElementsByClassName("d8cD2XWD")[0].style.width = "850px";

var style = document.createElement('style');

// 定义要添加的CSS规则
style.innerHTML = `
  .k3s5qMFF {
    display: none;
  }

  .webcast-chatroom___nickname {
    padding-left: 20px;
  }
  
  span.u2QdU6ht {
    padding-left: 20px;
  }

  .webcast-chatroom___content-with-emoji-emoji {
    display: none;
  }
`;

// 将 <style> 元素添加到 <head>
document.head.appendChild(style);
```

配置文件：`config.json`，部分配置通过GUI修改，核心配置请手动修改。  

管理员权限运行 `python main.py` 后，会打开GUI，可以进行配置设置和程序开关。  

首次使用时，CnOCR会下载模型，请开启魔法或设置huggingface镜像源下载。  



# 鸣谢

- [CnOCR](https://github.com/breezedeus/CnOCR)

# 更新日志

- 2024-10-08
    - 初版demo发布
