import os
from flask import Flask, request, jsonify, send_file
from upscale import celery, upscale
from flask.views import MethodView
from celery.result import AsyncResult
import webbrowser



app = Flask('app')
UPLOAD_FOLDER = r'D:\PyProject\Netology\Celery_homework'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
celery.conf.update(app.config)


class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)


class ImageScale(MethodView):

    def post(self):
        input_file = request.form.get('input_file')
        output_file = request.form.get('output_file')
        task = upscale.delay(input_file, output_file)
        return jsonify(
            {'task_id': task.id}
        )

    def get(self, task_id):
        task = AsyncResult(task_id, app=celery)
        return jsonify({
            'status': task.status,
            'result': task.result,
        })


class FinalImage(MethodView):

    def get(self, file_name):
        filename = os.path.join(UPLOAD_FOLDER, file_name)
        webbrowser.open(filename)
        return "ok"


def flask_test():
    return "ok"



app.add_url_rule("/", view_func=flask_test, methods=["GET"])
app.add_url_rule("/upscale", view_func=ImageScale.as_view('upscale'), methods=["POST"])
app.add_url_rule("/tasks/<string:task_id>", view_func=ImageScale.as_view('tasks'), methods=["GET"])
app.add_url_rule("/processed/<file_name>", view_func=FinalImage.as_view('processed'), methods=["GET"])

if __name__ == "__main__":
    app.run()

