from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import os
from PIL import Image

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
def read_image(filename, target_size=(224, 224)):
    img = load_img(filename, target_size=target_size)
    x = img_to_array(img)
    x = np.expand_dims(x, axis=0)
    return x

# Function to compress the image before saving
def compress_image(image, output_path, quality=85):
    image.save(output_path, optimize=True, quality=quality)

# Function to resize the image before saving
def resize_image(image, output_path, target_size=(224, 224)):
    resized_image = image.resize(target_size)
    resized_image.save(output_path)

UPLOAD_FOLDER = 'static/images'

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = file.filename
            file_path = os.path.join(UPLOAD_FOLDER, filename)

            # Compress and resize the image before saving
            image = Image.open(file)
            compress_image(image, file_path, quality=85)
            resize_image(image, file_path, target_size=(224, 224))

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
