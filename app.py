from flask import Flask, render_template, request, send_file
import os
from core.text_processing import process_text
from core.pdf_operations import create_pdf
from core.word_operations import create_word
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'txt'}

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'text' in request.form:
            text = request.form['text']
            questions = process_text(text)
            return render_template('results.html', questions=questions)
        elif 'file' in request.files:
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filename)
                with open(filename, 'r') as f:
                    text = f.read()
                questions = process_text(text)
                return render_template('results.html', questions=questions)
            else:
                return "Invalid file type", 400
    return render_template('index.html')

@app.route('/download_pdf')
def download_pdf():
    questions = request.args.getlist('questions')
    #print(questions)
    print("__________________")
    print("type of questions",type(questions))
    print("__________________")
    print("__________________",questions)
    jsoned_questions=json.dumps(questions)
    print("type of questions after json",type(questions))
    print("__________________")


    pdf_file = create_pdf(questions)
    return send_file(pdf_file, as_attachment=True, download_name='questions.pdf', mimetype='application/pdf')

@app.route('/download_word')
def download_word():
    questions = request.args.getlist('questions')
    word_file = create_word(questions)
    return send_file(word_file, as_attachment=True, download_name='questions.docx', mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')

if __name__ == '__main__':
    app.run(debug=True)
