import os
import cv2
import pytesseract
import string
import random
from textblob import TextBlob
from flask import (Flask, render_template, request, redirect, flash, url_for)
from werkzeug.utils import secure_filename
app = Flask(__name__)

UPLOAD_FOLDER = os.path.join('static', 'upload')
ALLOWED_EXTENSION = set(['png','jpeg','jpg'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSION

def getExtension(filename):
    return filename.split('.')[1].lower()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        file = request.files['gambar']
        alpha = request.form.get('alphabet')
        extension = getExtension(file.filename)

        if 'gambar' not in request.files:
            return redirect(request.url)

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'imageobject.' + extension))

            return redirect(url_for('generate', ext=extension, alp=alpha))
    
    return render_template('index.html')

@app.route('/generate/<ext>/<alp>')
def generate(ext,alp):
    filename = 'imageobject.' + ext
    random_string = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
    full_filename = ('static/upload/'+filename)
    img = cv2.imread(full_filename)
    if alp == 'ara':
        text = pytesseract.image_to_string(img, lang='ara')
    else:
        text = pytesseract.image_to_string(img) 
    textBlb = TextBlob(text)
    textCorrected = textBlb.correct()

    return render_template('afterupload.html', text=textCorrected, filename='/'+full_filename+'?'+random_string)