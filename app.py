from flask import Flask,render_template,url_for
from fileinput import filename
from flask import *
from distutils import debug
import speech_recognition as sr
import os



app=Flask(__name__)
app.config['UPLOAD_EXTENSION']=['.wav']

if __name__=='__main__':
    app.run(debug=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/success',methods = ['POST'])
def success():
    if (request.method == 'POST' and request.files['file']):
        f=request.files['file']
        if f.filename!='':
            file_ext=os.path.splitext(f.filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSION']:
                return render_template('index.html',text='this file extension is not supported.Please upload .wav file')
            f.save(os.path.join(app.root_path,'static/audios/{0}'.format(f.filename)))
            textfile=Speech_to_text(os.path.join(app.root_path,'static/audios/{0}'.format(f.filename)))
            audio=url_for('static',filename='/audios/{0}'.format(f.filename))
            print(f.filename)
            return render_template('index.html',audio = audio,text=textfile)
       
    else:
        return render_template('index.html',text="Please select an file before uploading!")

def Speech_to_text(f):
    r=sr.Recognizer()
    with sr.AudioFile(f) as source:
        audio=r.record(source)
    try:
        text_file=r.recognize_whisper(audio,model='tiny')
        print(text_file)
        return text_file
    except sr.UnknownValueError as e:
        print("whisper error;{0}".format(e))
      


     

