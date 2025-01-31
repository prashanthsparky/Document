import re

def extract_details(text, document_type):
    details = {}
    text = text.replace('\n', ' ').strip()

    if document_type == 'driving_license':

        # License Number, Name, DOB (with multilingual support)
        license_number_match = re.search(r'(DL|License|License No|DL No)\s*[:\-]?\s*([A-Z0-9\-]+)', text)
        name_match = re.search(r'Name\s*[:\-]?\s*([A-Za-z\s]+)', text)
        dob_match = re.search(r'(DOB|Date of Birth|जनम दिन|जन्म तिथि)\s*[:\-]?\s*([\d\-\/]+)', text)

        details['document_number'] = license_number_match.group(2) if license_number_match else 'Not Found'
        details['name'] = name_match.group(1) if name_match else 'Not Found'
        details['date_of_birth'] = dob_match.group(2) if dob_match else 'Not Found'
        
    elif document_type == 'adhar':
        name_match = re.search(r'Name\s*[:\-]?\s*([A-Za-z\s]+)', text)
        dob_match = re.search(r'(DOB|ಜನ್ಮ ದಿನಾಂಕ|जन्म तिथि)\s*[:\-]?\s*([\d\-]+)', text)
        aadhaar_number_match = re.search(r'Aadhaar\s*No\s*[:\-]?\s*([\d\s]+)', text)

        details['document_number'] = aadhaar_number_match.group(1) if aadhaar_number_match else 'Not Found'
        details['name'] = name_match.group(1) if name_match else 'Not Found'
        details['date_of_birth'] = dob_match.group(2) if dob_match and dob_match.lastindex >= 2 else 'Not Found'

    elif document_type == 'pan':
        pan_number_match = re.search(r'Permanent Account Number\s*[:\-]?\s*([A-Z0-9]{10})', text)
        name_match = re.search(r'(नाम|Name)\s*[:\-]?\s*([A-Za-z\s]+)', text)
        dob_match = re.search(r'(जन्म की तारीख|Date of Birth)\s*[:\-]?\s*([\d\-\/]+)', text)

        # Make sure to use the correct groups
        details['document_number'] = pan_number_match.group(1) if pan_number_match else 'Not Found'
        details['name'] = name_match.group(2) if name_match else 'Not Found'
        details['date_of_birth'] = dob_match.group(2) if dob_match else 'Not Found'

    elif document_type == 'voter_id':
        voter_id_number_match = re.search(r'Voter\s*ID\s*No\s*[:\-]?\s*([A-Z0-9]+)', text)
        name_match = re.search(r'(नाम|Name)\s*[:\-]?\s*([A-Za-z\s]+)', text)
        dob_match = re.search(r'(Date of Birth|जन्म तिथि)\s*[:\-]?\s*([\d\-]+)', text)

        details['document_number'] = voter_id_number_match.group(1) if voter_id_number_match else 'Not Found'
        details['name'] = name_match.group(2) if name_match and name_match.lastindex >= 2 else 'Not Found'
        details['date_of_birth'] = dob_match.group(2) if dob_match and dob_match.lastindex >= 2 else 'Not Found'

    elif document_type == 'passport':
        passport_number_match = re.search(r'(पासपोर्ट न\.|Passport No)\s*[:\-]?\s*([A-Z0-9]+)', text)
        name_match = re.search(r'Given Name(s)\s*[:\-]?\s*([A-Za-z\s]+)', text)
        dob_match = re.search(r'(जन्मतिथि|Date of Birth)\s*[:\-]?\s*([\d\-]+)', text)

        details['document_number'] = passport_number_match.group(2) if passport_number_match and passport_number_match.lastindex >= 2 else 'Not Found'
        details['name'] = name_match.group(2) if name_match and name_match.lastindex >= 2 else 'Not Found'
        details['date_of_birth'] = dob_match.group(2) if dob_match and dob_match.lastindex >= 2 else 'Not Found'
         
    elif document_type == 'utility':
        # Extract details from Utility Bill
        name_match = re.search(r'Name\s*[:\-]?\s*([A-Za-z\s]+)', text)
        address_match = re.search(r'Address\s*[:\-]?\s*([^\d]+)', text)
        account_number_match = re.search(r'Account\s*No\s*[:\-]?\s*([\d]+)', text)
        # Extracting from other possible variations
        name_match = name_match or re.search(r'([A-Za-z\s]+)(?:[^\d]*Account)', text)
        account_number_match = account_number_match or re.search(r'([\d]+)[\s]*[Account|No]', text)

        details['document_number'] = account_number_match.group(1) if account_number_match else 'Not Found'
        details['name'] = name_match.group(1) if name_match else 'Not Found'
        details['date_of_birth'] = 'Not Found'

    return details
