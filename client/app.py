import os
from flask import Flask, request, render_template, jsonify
from PIL import Image
import base64
from ml_model import TFModel

UPLOAD_FOLDER = './static/uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

model = TFModel(model_dir='./ml-model/')
model.load()

@app.route('/bears', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file1' not in request.files:
            return 'there is no file1 in form!'
        file1 = request.files['file1']
        path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
        file1.save(path)

        image_1 = Image.open(path)
        outputs = model.predict(image_1)

        return render_template('prediction.html', pred_result=outputs)

    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True,use_reloader=True)