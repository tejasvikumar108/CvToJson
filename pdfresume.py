import json
from PyPDF2 import PdfReader

# Define the PDF file name
pdf_filename = "Resume.pdf"
json_filename = "resume.json"

# Function to extract text from the PDF file
def extract_text_from_pdf(pdf_filename):
    reader = PdfReader(pdf_filename)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Function to parse the extracted text into a structured dictionary
def parse_resume(text):
    lines = text.split('\n')
    resume_data = {
        "personal_details": {},
        "objective": "",
        "education": [],
        "experience": [],
        "skills": [],
        "projects": []
    }
    
    current_section = None
    
    for line in lines:
        line = line.strip()
        if line.lower() == "objective":
            current_section = "objective"
        elif line.lower() == "education":
            current_section = "education"
        elif line.lower() == "experience":
            current_section = "experience"
        elif line.lower() == "skills":
            current_section = "skills"
        elif line.lower() == "projects":
            current_section = "projects"
        elif line:
            if current_section == "objective":
                resume_data["objective"] += line + " "
            elif current_section == "education":
                resume_data["education"].append(line)
            elif current_section == "experience":
                resume_data["experience"].append(line)
            elif current_section == "skills":
                resume_data["skills"].append(line)
            elif current_section == "projects":
                resume_data["projects"].append(line)
            elif current_section is None:
                # Assuming the first lines are personal details
                if "name" not in resume_data["personal_details"]:
                    resume_data["personal_details"]["name"] = line
                elif "address" not in resume_data["personal_details"]:
                    resume_data["personal_details"]["address"] = line
                elif "email" not in resume_data["personal_details"]:
                    resume_data["personal_details"]["email"] = line
                elif "phone" not in resume_data["personal_details"]:
                    resume_data["personal_details"]["phone"] = line
    
    # Clean up the objective field
    resume_data["objective"] = resume_data["objective"].strip()
    
    return resume_data

# Extract text from the PDF
extracted_text = extract_text_from_pdf(pdf_filename)

# Parse the extracted text
parsed_data = parse_resume(extracted_text)

# Write the parsed data to a JSON file
with open(json_filename, 'w') as json_file:
    json.dump(parsed_data, json_file, indent=4)

print(f"Resume data has been written to {json_filename}")
