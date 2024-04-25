from flask import Flask, render_template, request, jsonify, session
import os
from pdfToText import extract_text_from_pdf
from get_summary import summarize_resume
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['summaryDB']
collection = db['summaries']

# Define the folder where uploaded files will be stored
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key = 'your_secret_key'

global summary_text

@app.route('/', methods=['GET', 'POST'])
def index():
    
    if request.method == 'POST':
        # Handle file upload here
        if 'file' not in request.files:
            return 'No file part'
        
        file = request.files['file']
        
        if file.filename == '':
            return 'No selected file'
        
        # Save the uploaded file to the designated folder
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        
        # Clear old resume_text from session
        print("Before clearing session:", session.get('resume_text'))
        session.pop('resume_text', None)
        print("After clearing session:", session.get('resume_text'))
        
        # Extract text from the uploaded PDF file
        extracted_data = extract_text_from_pdf(file_path)
        text = extracted_data['text']
        session['resume_text'] = extracted_data['text']  # Save text to session
        session['metadata'] = extracted_data['metadata']
        
        return 'File uploaded successfully!'
    
    # Retrieve summary from the session if available
    resume_text = session.get('resume_text')
    metadata = session.get('metadata', {})  
    
    return render_template('index.html', resume_text=resume_text, metadata=metadata)



@app.route('/summarize', methods=['POST'])
def summarize():
    resume_text = session.get('resume_text')
    #print(resume_text)
    if not resume_text:
        return 'Resume text not available'
    
    summary = summarize_resume(resume_text)
    
    # Save the summary to the session
    session['summary_text'] = summary
    
    return summary


@app.route('/save-summary', methods=['POST'])
def save_summary():
    pdf_name = request.form.get('pdfName')
    summary_text = request.form.get('summaryText')
    
    if not pdf_name or not summary_text:
        return 'Missing PDF name or summary text'
    
    # Save the summary and PDF name to the database
    summary_data = {
        'pdfName': pdf_name,
        'summary': summary_text
    }
    # Update existing entry if it exists, or insert a new one
    collection.update_one({'pdfName': pdf_name}, {'$set': summary_data}, upsert=True)
    
    return 'Summary saved successfully!'

@app.route('/get-saved-summaries', methods=['GET'])
def get_saved_summaries():
    saved_summaries = list(collection.find({}, {'_id': False}))  # Fetch all saved summaries from the database
    return jsonify(saved_summaries)

@app.route('/delete-summary', methods=['POST'])
def delete_summary():
    pdf_name = request.form.get('pdfName')
    if not pdf_name:
        return 'PDF name not provided', 400

    # Delete the summary from the database based on the PDF name
    result = collection.delete_one({'pdfName': pdf_name})
    if result.deleted_count == 0:
        return 'Summary not found', 404

    return 'Summary deleted successfully'


if __name__ == '__main__':
    app.run(debug=True)
