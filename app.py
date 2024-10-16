import asyncio
import subprocess
import time
from fastapi import FastAPI, File, UploadFile, HTTPException
from PIL import Image
from io import BytesIO
from transparent_background import Remover, picture_compression
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
        start_time = time.time()  # 记录开始时间

        out = remover.process(img)

        end_time = time.time()  # 记录结束时间

        # 计算运行时长
        duration = end_time - start_time

        print("运行时长：", duration, "秒")
        
        #out = out.convert('RGB')
        
        buffered = BytesIO()  # 创建一个 BytesIO 对象
        out.save(buffered, format="PNG", optimize=True, quality=50)  # 将处理后的图像保存到 BytesIO 对象中

        buffered.seek(0)  # 将文件指针移动到文件开头
        return StreamingResponse(buffered, media_type="image/png")  # 返回处理后的图像数据
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  # 如果出现异常，则返回服务器错误状态码和错误信息


@app.post("/test/")
async def test():
    try:
        # 返回一个简单的响应
        return {"message": "Hello, World!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  # 如果出现异常，则返回服务器错误状态码和错误信息


import aiofiles

async def process_image(input_path, output_path, remover):
    try:
        start_time = time.time()  # Record start time
        # Open and compress input image
        async with aiofiles.open(input_path, "rb") as f:
            img_data = await f.read()
        img = Image.open(BytesIO(img_data)).convert('RGB')
        
        # Get image size and calculate compression quality
        image_size = img.width * img.height
        quality = picture_compression.calculate_quality(image_size)

        # Compress image
        buffer = BytesIO()
        img.save(buffer, format='JPEG', quality=quality, optimize=True)
        buffer.seek(0)
        img = Image.open(buffer)

        # Process image (Replace this with your image processing logic)
        out = remover.process(img)

        # Simulate some processing time
        await asyncio.sleep(1)
        
        async def save_image(output_path, out):
            async with aiofiles.open(output_path, "wb") as f:
                buffer = BytesIO()
                out.save(buffer, format='PNG', quality=80)
                buffer.seek(0)
                await f.write(buffer.read())

        await save_image(output_path, out)

        end_time = time.time()  # Record end time
        # Calculate duration
        duration = end_time - start_time
        print("Processing time:", duration, "seconds")
        # Return success message
        return {"message": "Image processed and saved successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/remove_background_performance/")
async def remove_background(input_path: str, output_path: str):
    print(input_path, output_path)
    try:
        # Process image asynchronously
        result = await process_image(input_path, output_path, remover)

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/shutdown/")
async def shutdown_server():
    # 执行系统关机命令
    subprocess.run(["shutdown", "/s", "/t", "1"])
    #print("shut")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
