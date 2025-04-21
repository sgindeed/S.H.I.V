import os
from flask import Flask, request, render_template
import tempfile
from utils import extract_text_from_pdf, extract_text_from_word, extract_text_from_ppt, process_image_and_get_prompt
from ml_utils import generate_answer, generate_answer_with_image

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx', 'ppt', 'pptx', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    answer = None
    error = None
    if request.method == 'POST':
        if 'file' not in request.files:
            error = 'No file part'
            return render_template('index.html', error=error)
        file = request.files['file']
        question = request.form.get('question')

        if file.filename == '':
            error = 'No selected file'
            return render_template('index.html', error=error)

        if file and question and allowed_file(file.filename):
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                file.save(tmp_file.name)
                file_path = tmp_file.name
                file_extension = file.filename.rsplit('.', 1)[1].lower()
                file_content_type = file.content_type

            if file_extension in ['txt', 'pdf', 'doc', 'docx', 'ppt', 'pptx']:
                if file_extension == 'pdf':
                    text_content = extract_text_from_pdf(file_path)
                elif file_extension in ['doc', 'docx']:
                    text_content = extract_text_from_word(file_path)
                elif file_extension in ['ppt', 'pptx']:
                    text_content = extract_text_from_ppt(file_path)
                else:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        text_content = f.read()

                if text_content:
                    prompt = f"Based on the following content:\n\n{text_content}\n\nAnswer the question: {question}"
                    answer, error = generate_answer(prompt)
                else:
                    error = "Could not extract text from the uploaded document."

            elif file_content_type.startswith('image/'):
                prompt_parts, err = process_image_and_get_prompt(file_path, question)
                if prompt_parts:
                    answer, error = generate_answer_with_image(prompt_parts)
                else:
                    error = err

            else:
                error = f"Unsupported file type: {file.content_type}"

            os.unlink(file_path)  # Clean up the temporary file

    return render_template('index.html', answer=answer, error=error)

if __name__ == '__main__':
    app.run(debug=True)