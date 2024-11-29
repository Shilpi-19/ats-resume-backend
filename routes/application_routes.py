# from flask import Blueprint, request, jsonify
# from services.llm_service import parse_resume, clean_and_parse_response
# from services.db_service import insert_application
# application_bp = Blueprint('application_bp', __name__)
# import base64

# # @application_bp.route('/applications', methods=['POST'])
# # def handle_application():
# #     name = request.form.get('name')
# #     email = request.form.get('email')
# #     resume = request.files.get('resume')

# #     if not name or not email or not resume:
# #         return jsonify({"error": "Missing data"}), 400

# #     # Save or process the resume
# #     return jsonify({"message": "Application received", "name": name, "email": email}), 201

# # 


# @application_bp.route('/applications', methods=['POST'])
# def handle_application():
#     print("Form Data:", request.form)
#     print("Files Data:", request.files)

#     name = request.form.get('name')
#     email = request.form.get('email')
#     resume = request.files.get('resume')

#     if not name or not email or not resume:
#         print("Missing fields:", name, email, resume)
#         return jsonify({"error": "Missing data"}), 400

#     try:
#         # Read and encode the resume content
#         resume_data = resume.read()
#         print("Resume Data Size:", len(resume_data))

#         # Optionally base64 encode if required
#         resume_encoded = base64.b64encode(resume_data).decode('utf-8')

#         response = parse_resume(resume_encoded)  # Ensure parse_resume supports binary input
#         print("Parsed Response:", response)

#         clean_response = clean_and_parse_response(response)
#         print("Cleaned Response:", clean_response)

#         # Insert the application into MongoDB
#         result = insert_application({
#             "name": name,
#             "email": email,
#             "resume": clean_response  # Ensure compatibility with MongoDB schema
#         })
#         print("Application Inserted, ID:", result.inserted_id)

#         return jsonify({
#             "name": name,
#             "email": email,
#             "resume": clean_response
#         }), 201

#     except Exception as e:
#         print(f"Error handling application: {e}")
#         return jsonify({"error": "Failed to process application"}), 500

import os
from flask import request, jsonify
from werkzeug.utils import secure_filename
from flask import Blueprint, request, jsonify
from services.llm_service import parse_resume, clean_and_parse_response
from services.db_service import insert_application,is_email_unique
application_bp = Blueprint('application_bp', __name__)
 
UPLOAD_FOLDER = 'uploads'  # Define the upload directory
ALLOWED_EXTENSIONS = {'pdf'}  # Allowed file extensions
 
# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
 
def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
 
@application_bp.route('/applications', methods=['POST'])
def handle_application():
    try:
        print("Form Data:", request.form)
        print("Files Data:", request.files)
 
        # Extract form fields
        name = request.form.get('name')
        email = request.form.get('email')
        resume = request.files.get('resume')  # File input
 
        # Validate required fields
        if not name or not email or not resume:
            print("Missing fields:", name, email, resume)
            return jsonify({"error": "Missing data"}), 400
        if not is_email_unique(email):
                    return jsonify({"error": "Email already exists"}), 400
        # Validate file type
        if not allowed_file(resume.filename):
            return jsonify({"error": "Only PDF files are allowed"}), 400
 
        # Secure and save the uploaded file
        filename = secure_filename(resume.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        resume.save(file_path)  # Save file to the upload folder
        print(f"File saved to {file_path}")
 
        # Process the saved file
        parsed_data = parse_resume(file_path)
        # if not parsed_data:
        #     return jsonify({"error": "Failed to parse resume"}), 400
        # elif parsed_data.get('out_of_format'):
        #     return jsonify({"error": "Resume is not in the correct format"}), 400
        # elif parsed_data.get('evaluation_score') == 0:
        #     return jsonify({"error": "Uploaded resume does not align with our domains"}), 400
 
        # Insert the application into MongoDB

        # result = insert_application({
        #     "name": name,
        #     "email": email,
        #     "resume_path": file_path,  # Save the file path instead of the content
        #     "parsed_data": parsed_data  # Include parsed resume data
        # })
        # print("Application Inserted, ID:", result.inserted_id)
        clean_response = clean_and_parse_response(parsed_data)
        print("Cleaned Response:", clean_response)

        # Insert the application into MongoDB
        result = insert_application({
            "name": name,
            "email": email,
            "resume": clean_response  # Ensure compatibility with MongoDB schema
        })
        print("Application Inserted, ID:", result.inserted_id)
 
        return jsonify({"Status":"Resume Uploaded Successfully"}), 201
 
    except Exception as e:
        print(f"Error handling application: {e}")
        return jsonify({"error": "Failed to process application"}), 500