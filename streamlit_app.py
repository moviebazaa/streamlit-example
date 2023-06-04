from flask import Flask, render_template, request, redirect, send_file
import pysrt
from translate import Translator

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    # Get the uploaded .srt file from the form
    srt_file = request.files['srt_file']

    # Read the .srt file using pysrt library
    subs = pysrt.open(srt_file)
    
    # Get the target language from the form
    target_language = request.form['target_language']
    
    # Translate each subtitle in the .srt file
    translator = Translator(to_lang=target_language)
    for sub in subs:
        translated_text = translator.translate(sub.text)
        sub.text = translated_text
    
    # Save the translated .srt file
    translated_filename = f"translated_{srt_file.filename}"
    subs.save(translated_filename, encoding='utf-8')

    # Return the translated file for download
    return send_file(translated_filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
