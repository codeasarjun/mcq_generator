from flask import Flask, render_template, request, send_file,redirect, url_for, flash
import os
from core.text_processing import process_text
from core.pdf_operations import create_pdf
from core.word_operations import create_word
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'txt'}

try:
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
except PermissionError as e:
    print(f"PermissionError: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")


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

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        # Process the contact information here (e.g., save to database or send email)
        flash('Thank you for contacting us!', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        feedback = request.form.get('feedback')
        flash('Thank you for your feedback!', 'success')
        return redirect(url_for('feedback'))
    return render_template('feedback.html')

if __name__ == '__main__':
    app.run(debug=True)
