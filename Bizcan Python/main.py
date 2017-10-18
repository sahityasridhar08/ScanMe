import sqlite3,json
from flask import Flask, render_template, request, redirect, url_for, send_from_directory,session, url_for
import pytesseract as pyt
#import barcode as bc
import os
from PIL import Image
import pyqrcode 
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg'])
#For Barcode
#EAN = bc.get_barcode_class('ean13')

def ret_string(filename):
    im=Image.open(app.config['UPLOAD_FOLDER']+str(filename))
    return pyt.image_to_string(im, lang='eng')

def create_file(filename,data):
    filename=filename[:len(filename)-4]
    qrc=pyqrcode.create(str(data))
    fname="q"+filename+".png"
    qrc.png(app.config['UPLOAD_FOLDER']+fname, scale=8)
    print(qrc.terminal(quiet_zone=1))
    #For Barcode
    #ean =  EAN(data, writer=bc.ImageWriter())
    #fname=ean.save(filename)
    return str(fname)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/getNoteText',methods=['GET','POST'])
def GetNoteText():
    if request.method == 'POST':
        file = request.files['pic']
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        data=ret_string(filename)
        return create_file(filename,data)
    else:
        return "Sorry, Try again"



if __name__ == '__main__':
    app.secret_key = 'abc123'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='0.0.0.0',port=3000,debug=True)
