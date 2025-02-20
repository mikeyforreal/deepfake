from flask import Flask, flash, request, redirect, render_template, url_for
import os

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'wmv'}

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Make sure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if post request has file
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            flash('File successfully uploaded')
            return render_template('upload.html', filename=file.filename)
        else:
            flash('Allowed file types are mp4, avi, mov, wmv')
            return redirect(request.url)
    return render_template('upload.html')

@app.route('/display/<filename>')
def display_video(filename):
    return redirect(url_for('static', filename='uploads/' + filename))

@app.route('/predict/<filename>')
def sequence_prediction(filename):
    # Placeholder for actual prediction logic
    # In a real implementation, you would call your model here
    import random
    result = "REAL" if random.random() > 0.5 else "FAKE"
    return render_template('upload.html', filename=filename, prediction=result)

if __name__ == '__main__':
    print("Starting DeepFake Detection server...")
    print("Open http://127.0.0.1:5000 in your web browser")
    app.run(debug=True)