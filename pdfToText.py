import os
import PyPDF2

def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        file_size = os.path.getsize(file_path)  # Get the size of the file
        reader = PyPDF2.PdfReader(file)
        metadata = reader.metadata
        num_pages = len(reader.pages)
        text = ''
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text += page.extract_text()
    return {'metadata': metadata, 'text': text, 'file_size': file_size}





# if __name__ == '__main__':
#     extracted_text = extract_text_from_pdf(
#         "C:/Users/varun/PycharmProjects/summaryAI/uploads/CHADUVULA-VARUN-FlowCV-Resume-20240211.pdf")
#     print(extracted_text)
