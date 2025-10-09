

import os
import re
from PyPDF2 import PdfReader, PdfWriter
from pdf_page_numbers import list_of_pdfs # Importing the list from another file
from pdf_names import pdf_names # Importing the list from another file
from pdf_categories import categories # Importing the list from another file
from pdf_article_levels import article_levels # Importing the list from another file
from pdf2image import convert_from_path



# pdf_source_name = "English Digest_May 2025.pdf"
# pdf_source_name = pdf_source_name.replace(".pdf", "")



# Creating sub-pdf from source pdf given the page ranges
def extract_pages(pdf_source_name_path, pdf_b_path, start_page, end_page):
    """
    Creates PDF B from PDF A given the page range [start_page, end_page] (1-based, inclusive).
    """
    reader = PdfReader("./uploads/" + pdf_source_name_path)
    writer = PdfWriter()
    # Adjust for 0-based indexing
    for i in range(start_page - 1, end_page):
        writer.add_page(reader.pages[i])
    with open(pdf_b_path, "wb") as out_file:
        writer.write(out_file) 


# Extracting text from pdf using OCR
def extract_text_from_pdf(pdf_path):
    """Extracting text from pdf using OCR"""

    import pytesseract

    # Convert PDF to a list of images
    images = convert_from_path(pdf_path)

    # Extract text from each image
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img)

    return text


# Create directory for sub-pdfs creation
def create_dir(name):
    """Create directory for sub-pdfs creation"""
    if not os.path.exists(f'./extracted/{name}'):
        print(f"Creating directory ./extracted/{name}...")
        os.makedirs(f'./extracted/{name}')
    else:
        # remove all files from directory
        for filename in os.listdir(f'./extracted/{name}'):
            file_path = os.path.join(f'./extracted/{name}', filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    import shutil
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')
    
    print(f"Directory ./extracted/{name} is ready.")


# Main function to generate sub-pdf extractions
def generate_pdf_extractions( file, tuples ):
    file = file.split('/')[-1]

    # Basic validation of pdfs lists and names
    # if len(list_of_pdfs)-1 != len(pdf_names):
    #     print(f'Warning: The number of PDF files and names do not match: {len(list_of_pdfs)-1} != {len(pdf_names)}')
    #     exit(1)


    # Creating sub-pdfs from source pdf
    create_dir(name=file)
    print("extracting files...")
    
    order = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    order.reverse()

    # get the number of pages in the source pdf
    reader = PdfReader("./uploads/" + file )
    file_size = len(reader.pages)

    for i in range(len(tuples)):
        if tuples[i]['title'].replace(" ", "").lower() != "none":
            new_pdf_name = f"{order.pop()}_category*" + "-" + tuples[i]['title'] + "-" + file.lower().replace(".pdf", "") + '-Level-' + tuples[i]['level']
            new_pdf_name = new_pdf_name.title().replace("  ", " ").replace(" ", "_").replace(":", "").replace("__", "_").replace("&", "and")
            extracted_pdf = f"./extracted/{file}/{new_pdf_name}.pdf"
            start_page = tuples[i]['page']
            end_page = tuples[i + 1]['page']-1 if i + 1 < len(tuples) else file_size
            extract_pages(file, extracted_pdf, start_page, end_page)

        # if pdf_names[i] != "None" and pdf_names[i] != "none":
        #     new_pdf_name = f"{order[i]}_category" + "-" + pdf_names[i] + "-" + pdf_source_name + ' Level'
        #     new_pdf_name = new_pdf_name.title().replace("  ", " ").replace(" ", "_").replace(":", "").replace("’", "").replace("'", "").replace("&", "and")
        #     pdf_b = f"./extracted/{pdf_source_name}/{new_pdf_name}.pdf"
        #     start_page = list_of_pdfs[i]
        #     end_page = list_of_pdfs[i + 1]-1
        #     extract_pages(pdf_source_name, pdf_b, start_page, end_page)
        #     print(f"\t{new_pdf_name}")

    print("Extraction completed.")


     # Extracting text from each sub-pdf and saving to a .txt file

    print("Extracting text from pdfs using OCR...")

    #
    dict_of_pdf_texts = []

    import json

    for filename in sorted(os.listdir(f'./extracted/{file}')):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(f'./extracted/{file}', filename)
            dict_of_pdf_texts.append({ "title": filename, "text" : re.sub(r'[^a-zA-Z0-9 .,?!:;\'"-]', '',extract_text_from_pdf(pdf_path).replace("\n", " ").replace("\t", " ").replace("  ", " ")[:1000]) })
            # break

    # dict_of_pdf_texts = f'{{ "articles": {dict_of_pdf_texts} }}'

    with open(f'./extracted/{file}/prompt.json', "w", encoding="utf-8") as text_file:
        prompt = f"""You are a helpful English assistant that helps to classify articles for ESL students into categories based on their title and more importantly on the content (vocab and sentence structure).
        Please use the following rules or criteria for classifying articles. 
        Please return an array of categories names.
        1. The categories should be determined by the article title AND the content of the article matching to the following list: {categories.__str__()}
        2. You must strictly follow the categories provided in the list above. Do not create your own categories nor use other titles that are not in the data provided.
        3. If the article title is not clear, then you must rely on the content of the article to determine the category.
        4. You must implement the chain of thought reasoning. This means you must reason in steps before concluding the final category. Note that the reasoning should not be outputed, only the final category should be outputted.
        5. After concluding the reasoning, you must provide the final category name only. No comments or explanations in python syntax: [ c_0, c_1, ..., c_k ]

        Below is the data obtained from OCR extraction of {len(dict_of_pdf_texts)} articles containing their respective articles titles and the content of the articles:\n
        
        JSON data:\n"""
        # print(prompt)
        text_file.write(prompt)
        json.dump(dict_of_pdf_texts, text_file, indent=4, ensure_ascii=False)


    print(f"Extraction completed and saved to ./extracted/{file}/prompt.txt.")

    print("Please copy prompt from prompt.txt and paste it into chatGPT.com. Then return to paste the output.")




# path = './uploads/English_Digest_May_2025.pdf'
# pages =  [{'page': 2, 'title': 'lei day'}, {'page': 5, 'title': 'none'}, {'page': 68, 'title': 'brunch'}, {'page': 70, 'title': 'none'}]
# generate_pdf_extractions(path, pages)
