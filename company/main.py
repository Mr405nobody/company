#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主启动器：已将原有的 tkinter GUI 替换为 Streamlit 网页应用。

说明：
- 请使用 `streamlit run app.py` 启动网页界面（仓库中已包含 `app.py`）。
- 运行此脚本会尝试调用系统的 `streamlit` 命令以启动服务，若未安装会给出提示。

原 tkinter 实现已迁移到 `app.py`（Streamlit）。保留此启动脚本以便用户无缝切换。
"""

import os
import sys
import shutil
import subprocess


def main():
    # 首先检查 streamlit 是否可用
    if shutil.which("streamlit") is None:
        print("未检测到 streamlit 命令。请先安装依赖：")
        print("  pip install -r requirements.txt")
        print("然后运行：")
        print("  streamlit run app.py")
        sys.exit(1)

    repo_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(repo_dir, "app.py")
    if not os.path.exists(app_path):
        print("找不到 app.py，请确认仓库中包含 Streamlit 前端文件。")
        sys.exit(1)

    # 使用 execvp 替换当前进程为 streamlit，便于用户直接看到 streamlit 输出
    cmd = ["streamlit", "run", app_path]
    os.execvp(cmd[0], cmd)


if __name__ == "__main__":
    main()
