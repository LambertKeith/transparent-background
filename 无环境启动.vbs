Set WshShell = CreateObject("WScript.Shell")

' 安装依赖
WshShell.Run "cmd /c pip install -r .\requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple some-package", 0, True

' 启动 Uvicorn 服务器
WshShell.Run "cmd /c uvicorn app:app --host 0.0.0.0 --port 8000", 0, False