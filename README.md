<div align="center">
  <a href="#">
    <img src="https://raw.githubusercontent.com/LuoXi-Project/LX_Project_Template/refs/heads/main/ui/logo.png" width="240" height="240" alt="点我跳转文档">
  </a>
</div>

<div align="center">

# ✨ 洛曦 OCR数据监听  ✨

[![][python]][python]
[![][github-release-shield]][github-release-link]
[![][github-stars-shield]][github-stars-link]
[![][github-forks-shield]][github-forks-link]
[![][github-issues-shield]][github-issues-link]  
[![][github-contributors-shield]][github-contributors-link]
[![][github-license-shield]][github-license-link]

</div>

## 前言

基于tkinter开发，使用pyautogui进行屏幕截图，使用CnOCR进行文本识别，最后通过websocket，将解析后的数据发送给所有连接的客户端。

<a href="https://www.bilibili.com/video/BV1pB2NYLEoy" target="_blank">▶︎ 视频教程</span></a>

## 环境

python: 3.10  

## 安装

安装依赖：`pip install -r requirements.txt`  

## 运行

补充  
ws连接地址：ws://127.0.0.1:8765  

### 抖音

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

## 💡 提问的智慧

提交issues前请先阅读以下内容

https://lug.ustc.edu.cn/wiki/doc/smart-questions

## 🀅 开发&项目相关

可以使用 GitHub Codespaces 进行在线开发：

[![][github-codespace-shield]][github-codespace-link]  


## ⭐️ Star 经历

[![Star History Chart](https://api.star-history.com/svg?repos=Ikaros-521/ocr_data_monitor&type=Date)](https://star-history.com/#Ikaros-521/ocr_data_monitor&Date)



## 鸣谢

- [CnOCR](https://github.com/breezedeus/CnOCR)

## 更新日志

- 2024-10-08
    - 初版demo发布


[python]: https://img.shields.io/badge/python-3.10+-blue.svg?labelColor=black
[back-to-top]: https://img.shields.io/badge/-BACK_TO_TOP-black?style=flat-square
[github-action-release-link]: https://github.com/actions/workflows/Ikaros-521/ocr_data_monitor/release.yml
[github-action-release-shield]: https://img.shields.io/github/actions/workflow/status/Ikaros-521/ocr_data_monitor/release.yml?label=release&labelColor=black&logo=githubactions&logoColor=white&style=flat-square
[github-action-test-link]: https://github.com/actions/workflows/Ikaros-521/ocr_data_monitor/test.yml
[github-action-test-shield]: https://img.shields.io/github/actions/workflow/status/Ikaros-521/ocr_data_monitor/test.yml?label=test&labelColor=black&logo=githubactions&logoColor=white&style=flat-square
[github-codespace-link]: https://codespaces.new/Ikaros-521/ocr_data_monitor
[github-codespace-shield]: https://github.com/codespaces/badge.svg
[github-contributors-link]: https://github.com/Ikaros-521/ocr_data_monitor/graphs/contributors
[github-contributors-shield]: https://img.shields.io/github/contributors/Ikaros-521/ocr_data_monitor?color=c4f042&labelColor=black&style=flat-square
[github-forks-link]: https://github.com/Ikaros-521/ocr_data_monitor/network/members
[github-forks-shield]: https://img.shields.io/github/forks/Ikaros-521/ocr_data_monitor?color=8ae8ff&labelColor=black&style=flat-square
[github-issues-link]: https://github.com/Ikaros-521/ocr_data_monitor/issues
[github-issues-shield]: https://img.shields.io/github/issues/Ikaros-521/ocr_data_monitor?color=ff80eb&labelColor=black&style=flat-square
[github-license-link]: https://github.com/Ikaros-521/ocr_data_monitor/blob/main/LICENSE
[github-license-shield]: https://img.shields.io/github/license/Ikaros-521/ocr_data_monitor?color=white&labelColor=black&style=flat-square
[github-release-link]: https://github.com/Ikaros-521/ocr_data_monitor/releases
[github-release-shield]: https://img.shields.io/github/v/release/Ikaros-521/ocr_data_monitor?color=369eff&labelColor=black&logo=github&style=flat-square
[github-releasedate-link]: https://github.com/Ikaros-521/ocr_data_monitor/releases
[github-releasedate-shield]: https://img.shields.io/github/release-date/Ikaros-521/ocr_data_monitor?labelColor=black&style=flat-square
[github-stars-link]: https://github.com/Ikaros-521/ocr_data_monitor/network/stargazers
[github-stars-shield]: https://img.shields.io/github/stars/Ikaros-521/ocr_data_monitor?color=ffcb47&labelColor=black&style=flat-square
[pr-welcome-link]: https://github.com/Ikaros-521/ocr_data_monitor/pulls
[pr-welcome-shield]: https://img.shields.io/badge/%F0%9F%A4%AF%20PR%20WELCOME-%E2%86%92-ffcb47?labelColor=black&style=for-the-badge
[profile-link]: https://github.com/Ikaros-521

