from flask import Flask, render_template, request
from keras.models import load_model
import numpy as np
from keras.preprocessing.image import load_img, img_to_array
import os

app = Flask(__name__, template_folder='.')
model = load_model('s2augm.h5')
target_img = os.path.join(os.getcwd(), 'static/images')

@app.route('/')
def index_view():
    return render_template('index.html')

# Membolehkan file dengan ekstensi png, jpg, dan jpeg
ALLOWED_EXT = set(['jpg', 'jpeg', 'png'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT

# Fungsi untuk memuat dan mempersiapkan gambar dengan ukuran yang sesuai
def read_image(filename):
    img = load_img(filename, target_size=(224, 224))  # Ubah ukuran target menjadi (224, 224) sesuai dengan input shape model
    x = img_to_array(img)
    x = np.expand_dims(x, axis=0)
    return x

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = file.filename
            file_path = os.path.join('static/images', filename)
            file.save(file_path)
            img = read_image(file_path)
            class_prediction = model.predict(img)
            classes_x = np.argmax(class_prediction, axis=1)
            if classes_x == 0:
                cuaca = "Berawan"
            elif classes_x == 1:
                cuaca = "Cerah"
            elif classes_x == 2:
                cuaca = "Cerah Berawan"
            elif classes_x == 3:
                cuaca = "Hujan"
            else:
                cuaca = "Lainnya"
            return render_template('predict.html', cuaca=cuaca, prob=class_prediction, user_image=file_path)
        else:
            return "Tidak dapat membaca file. Silakan periksa ekstensi file"

if __name__ == '__main__':
    app.run(debug=True)
