# 蔬菜公司 Excel 助手 — Streamlit 网页化封装

此仓库原先为桌面 GUI（tkinter）应用，已将核心流程封装为一个可在本地或云端运行的 Streamlit 网页应用 `app.py`。

快速概览
- `app.py`：Streamlit 前端，复用仓库内模块（`parser.py`、`ocr_handler.py`、`price_table_handler.py`、`excel_handler.py`、`profit_calculator.py`）。
- `requirements.txt`：已加入 `streamlit`。

本地运行（推荐开发环境）

1. 创建并激活 Python 虚拟环境（macOS，zsh）：

```bash
cd /Users/guozuxiao/Documents/蔬菜小助手/company
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. 启动 Streamlit 应用：

```bash
streamlit run app.py
```

3. 浏览器打开 http://localhost:8501

使用说明
- 在“输入订单”中粘贴或编辑文字订单，点击“解析文字”。
- 在“定价表”上传图片（使用 OCR，需要腾讯云密钥）或上传 Excel。
- 在“进价表”上传进价 Excel。
- 在“生成与下载”生成利润表并下载 Excel 文件。

注意与建议
- OCR：仓库包含对腾讯云 OCR 的调用（`ocr_handler.py`），**请在生产环境不要把密钥写死到文件中**。建议修改 `ocr_handler.py` 从环境变量读取 `TENCENT_SECRET_ID`、`TENCENT_SECRET_KEY`，或在部署时注入环境变量。示例：

```python
import os
SECRET_ID = os.environ.get('TENCENT_SECRET_ID')
SECRET_KEY = os.environ.get('TENCENT_SECRET_KEY')
```

- 如果不使用 OCR，可仅使用 Excel 上传定价表与进价表。

部署建议

1) Streamlit Community Cloud（最快）：
   - 优点：免费、简单（连接 GitHub 后自动部署）。
   - 缺点：对环境变量和私密配置有限制。

步骤：
   - 将仓库 push 到 GitHub
   - 在 Streamlit Cloud 创建应用，指定 `app.py` 为入口
   - 在 Settings 添加必要环境变量（若使用 OCR）

2) Docker 部署到 VPS（推荐可控生产环境）：
   - 写一个基础 Dockerfile（基于 python:3.11），复制仓库，pip install -r requirements.txt，然后 CMD `streamlit run app.py --server.port 8501 --server.address 0.0.0.0`。
   - 在宿主机器上用 nginx 做反向代理并设置 TLS（Let’s Encrypt）。

3) 其他云（Heroku / Railway / Fly / VPS）：
   - 原理相同，确保在部署平台上设置环境变量并暴露端口。

质量验证
- 可运行 `python3 test_all.py`（仓库内已有测试脚本）来验证模块导入和核心流程。

下一步
- 若需要，我可以：
  - 把 `ocr_handler.py` 修改为从环境变量读取密钥（低风险改动）。
  - 编写示例 `Dockerfile` 与 `docker-compose.yml`。
  - 在 Streamlit Cloud 上给出一步步部署截图/说明。

— 结束 —
