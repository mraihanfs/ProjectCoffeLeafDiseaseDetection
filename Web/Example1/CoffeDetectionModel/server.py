import os
from flask import Flask, url_for, request
from flask.helpers import flash
from flask.templating import render_template
from werkzeug.utils import secure_filename
import tensorflow as tf
import numpy as np 
from keras.preprocessing import image 

app = Flask(__name__, template_folder='./')
app.config['UPLOAD_FOLDER'] = 'G:/My Drive/Kampus/Machine Learning/Web/Example1/startbootstrap-business-frontpage-gh-pages/static/temp'
model = tf.keras.models.load_model('static\model')

def prediction (imgPath):
    img = image.load_img(imgPath, target_size=(150,150))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x/=255
    value = np.vstack([x])
    classes = model.predict(value, batch_size=10)
    if classes >.5 :
        return True
    return False

@app.route('/')
def homeworld():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def ImageInput():
    file = request.files['img']
    fileName = secure_filename(file.filename)
    print(fileName)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], fileName))
    flag = prediction(os.path.join(app.config['UPLOAD_FOLDER'], fileName))
    return render_template('predictPage.html', imgName=fileName, flag=flag)

@app.route('/learnMore')
def learnMore():
    return render_template('learnMore.html')

app.run(host="0.0.0.0", debug=True, port=int(os.environ.get("PORT",5000)))

