from flask import Flask, render_template, request, redirect, url_for
from google.cloud import translate_v2 as translate
import os

# Initialize Flask app
app = Flask(__name__)

# Configure Google Translate API
translate_client = translate.Client()

# Function to translate subtitle file
def translate_subtitle(subtitle_path, target_language):
    # Read the subtitle file
    with open(subtitle_path, 'r', encoding='utf-8') as file:
        subtitle_text = file.read()

    # Translate the subtitle text
    translated_text = translate_client.translate(subtitle_text, target_language=target_language)

    # Return the translated text
    return translated_text['translatedText']

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route for handling file upload and translation
@app.route('/translate', methods=['POST'])
def translate():
    # Check if a file was uploaded
    if 'subtitle' not in request.files:
        return redirect(url_for('home'))

    # Get the uploaded file and target language from the form
    subtitle = request.files['subtitle']
    target_language = request.form['target_language']

    # Check if the file is valid
    if subtitle.filename == '':
        return redirect(url_for('home'))
    
    # Save the subtitle file to a temporary location
    subtitle_path = os.path.join('temp', subtitle.filename)
    subtitle.save(subtitle_path)

    # Translate the subtitle file
    translated_text = translate_subtitle(subtitle_path, target_language)

    # Delete the temporary subtitle file
    os.remove(subtitle_path)

    # Return the translated text to display on the website
    return translated_text

if __name__ == '__main__':
    # Create a 'temp' directory for temporary file storage
    if not os.path.exists('temp'):
        os.makedirs('temp')
    
    # Run the Flask app
    app.run(debug=True)
