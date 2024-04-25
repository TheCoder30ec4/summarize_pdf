import google.generativeai as genai
from pdfToText import extract_text_from_pdf



genai.configure(api_key="AIzaSyC4nAG6tfRuEjHPi32cmuI6ePY1oLPFg_4") 

# Set up the model
generation_config = {
    "temperature": 0.7,
    "max_output_tokens": 512  # Increased to 512 tokens
}

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest", generation_config=generation_config)

def summarize_resume(resume_text):
    prompt = f"Summarize this resume where check for skills, projects, achivements and cretifications.Make sure the resume is using action verbs and proper Grammer. Give it a score out of 10 and metion Strengths and weakness. Content: {resume_text}"
    response = model.generate_content(prompt)  
    #print(response.candidates[0])
    return response.text


