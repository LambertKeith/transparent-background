python -m venv .venv
call .venv\Scripts\activate.bat
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
uvicorn app:app --host 0.0.0.0 --port 8000 