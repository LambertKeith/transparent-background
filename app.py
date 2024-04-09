from fastapi import FastAPI, File, UploadFile, HTTPException
from PIL import Image
from io import BytesIO
from transparent_background import Remover
from starlette.responses import StreamingResponse

import os
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

app = FastAPI()

remover = Remover(mode='base', jit=False)  # 初始化 Remover 类

@app.post("/remove_background/")
async def remove_background(file: UploadFile = File(...)):
    try:
        contents = await file.read()  # 以二进制方式读取上传的文件内容
        img = Image.open(BytesIO(contents)).convert('RGB')  # 将文件内容转换为图像对象
        #out = remover.process(img, type='map')  # 使用 Remover 类处理图像
        out = remover.process(img)
        #out = out.convert('RGB')
        
        buffered = BytesIO()  # 创建一个 BytesIO 对象
        out.save(buffered, format="PNG", optimize=True, quality=50)  # 将处理后的图像保存到 BytesIO 对象中

        buffered.seek(0)  # 将文件指针移动到文件开头
        return StreamingResponse(buffered, media_type="image/png")  # 返回处理后的图像数据
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  # 如果出现异常，则返回服务器错误状态码和错误信息

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
