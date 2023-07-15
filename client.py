import time
import requests


def task_get(task_id):
    response = requests.get(f"http://127.0.0.1:5000/tasks/{task_id}")
    print()
    print(response.status_code)
    print(response.json())
    return response.json()


def image_post(input_path, output_path):
    data = {
        'input_file': input_path,
        'output_file': output_path
    }
    response = requests.post(
        "http://127.0.0.1:5000/upscale",
        data=data,
    )
    print()
    print(response.status_code)
    print(response.text)
    return response.json().get('task_id')


def image_get(file_name):
    response = requests.get(f"http://127.0.0.1:5000/processed/{file_name}")
    print()
    print(response.status_code)
    print(response.text)


if __name__ == "__main__":

    input_file_1 = "lama_300px.png"
    output_file_1 = "lama_600px.png"

    new_task = image_post(input_file_1, output_file_1)  # task_id
    status = "PENDING"
    while status == "PENDING":
        status = task_get(new_task).get('status')
        time.sleep(2)

    image_get(output_file_1)


