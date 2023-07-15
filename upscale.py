import cv2
from cv2 import dnn_superres
import shutil
from celery import Celery

import uuid


celery = Celery(
    'celery_app',
    backend='redis://localhost:6379/2',
    broker='redis://localhost:6379/1',
)


@celery.task
def upscale(input_path: str, output_path: str, model_path: str = 'EDSR_x2.pb') -> None:
    """
    :param input_path: путь к изображению для апскейла
    :param output_path:  путь к выходному файлу
    :param model_path: путь к ИИ модели
    :return:
    """

    scaler = dnn_superres.DnnSuperResImpl_create()
    scaler.readModel(model_path)
    scaler.setModel("edsr", 2)
    image = cv2.imread(input_path)
    result = scaler.upsample(image)
    cv2.imwrite(output_path, result)



def upscale2(input_path, output_path: str) -> str:
    with open(output_path, 'wb') as out:
        shutil.copyfileobj(input_path, out)
    random_id = uuid.uuid4()
    return str(random_id)


