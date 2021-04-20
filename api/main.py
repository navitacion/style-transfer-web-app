import uuid
import time
import cv2
import uvicorn
from fastapi import File
from fastapi import FastAPI
from fastapi import UploadFile
import numpy as np
from PIL import Image

import config
import inference

import asyncio
from concurrent.futures import ProcessPoolExecutor
from functools import partial


app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome from the API"}


@app.post("/{style}")
async def get_image(style: str, file: UploadFile = File(...)):
    image = np.array(Image.open(file.file))
    model = config.STYLES[style]
    start = time.time()
    output, resized = inference.inference(model, image)
    output_name = f"/storage/{str(uuid.uuid4())}.jpg"
    original_name = f"/storage/{str(uuid.uuid4())}.jpg"

    cv2.imwrite(output_name, output)
    cv2.imwrite(original_name, resized)
    models = config.STYLES.copy()
    del models[style]
    asyncio.create_task(generate_remaining_models(models, image, output_name))

    return {"name": output_name, "original": original_name, 'time': time.time() - start}


async def generate_remaining_models(models, image, name: str):
    executor = ProcessPoolExecutor()
    event_loop = asyncio.get_event_loop()
    await event_loop.run_in_executor(
        executor, partial(process_image, models, image, name)
    )


def process_image(models, image, name: str):
    for model in models:
        output, resized = inference.inference(models[model], image)
        name = name.split(".")[0]
        name = f"{name.split('_')[0]}_{models[model]}.jpg"
        cv2.imwrite(name, output)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)