from dotenv import load_dotenv
import os
import cohere
import PyPDF2
import json
from pypdf import PdfReader
load_dotenv()
co = cohere.Client(os.getenv("COHERE_API_KEY"))

api_key = os.getenv("COHERE_API_KEY")
if not api_key:
    print("COHERE_API_KEY not found!")
else:
    print("COHERE_API_KEY loaded successfully")

co = cohere.Client(api_key)



 
def pdfreader(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text += page.extract_text()
    return text


def parse_resume(resume_path):
    """
    This function handles the resume parsing logic.
    :param resume_path: Path to the uploaded resume PDF file.
    :return: Parsed resume result.
    """
    # Step 1: Extract text from the PDF
    resume_text = pdfreader(resume_path)

    # Step 2: Send the extracted text to the Cohere API for LLM parsing
    try:
        response = co.generate(
            model="command-xlarge-nightly",
            prompt=f'''Analyze the following resume to determine whether it is ATS-friendly. Provide an evaluation in JSON format, including the following fields:

            is_ats_friendly (true/false)
            missing_keywords (list of important keywords that are missing)
            format_issues (list of issues such as fonts, colors, tables, etc., that might make the resume less ATS-compatible)
            recommendations (specific suggestions for improvement to make it more ATS-friendly).
            Here is the resume: {resume_text}''',
            max_tokens=2000
        )
        return response.generations[0].text
    except Exception as e:
        return {"error": str(e)}
def clean_and_parse_response(llm_response: str) -> dict:
   raw_text = llm_response.replace('{', '{').replace('}', '}').strip()
   try:
    result = json.loads(raw_text)
    return result
   except json.JSONDecodeError as e:
    return(f"JSON decoding failed: {e}")    
   
# parse_resume = parse_resume(r"C:\Users\Dell\Downloads\Nandini-Tyagi-Resume-.pdf")
# print(parse_resume)
# print(clean_and_parse_response(parse_resume))
