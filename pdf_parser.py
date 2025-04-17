import fitz  # PyMuPDF
import re
import json

def extract_vaccine_info(pdf_path):
    doc = fitz.open(pdf_path)
    vaccine_data = {}

    text = ""
    for page in doc:
        text += page.get_text()

    # Normalize whitespace
    text = re.sub(r'\n+', '\n', text)

    # Common ages (used as keys)
    age_blocks = [
        "birth", "6 weeks", "10 weeks", "14 weeks",
        "6 months", "9 months", "12 months", "15 months",
        "18 months", "2 years", "5 years"
    ]

    # Pattern: Vaccine and Disease mentions under age groups
    for age in age_blocks:
        pattern = re.compile(rf"{age}.*?(?=(?:{'|'.join(age_blocks)}|\Z))", re.IGNORECASE | re.DOTALL)
        match = pattern.search(text)
        if match:
            block = match.group()
            vaccines = re.findall(r"([A-Za-z0-9\-+/() ]+):\s*(.*?)\n", block)
            cleaned = []
            for name, disease in vaccines:
                cleaned.append({
                    "vaccine": name.strip(),
                    "disease": disease.strip(),
                    "schedule": "NIP or IAP (unsure from raw text)"  
                })
            if cleaned:
                vaccine_data[age] = cleaned

    return vaccine_data

def save_as_json(data, output_file="vaccine_schedule.json"):
    with open(output_file, "w") as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    pdf_path = "D:\parentune\Immunization (1).pdf"
    data = extract_vaccine_info(pdf_path)
    save_as_json(data)
    print("Vaccine data extracted and saved to vaccine_schedule.json")
