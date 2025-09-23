

import os
from PyPDF2 import PdfReader, PdfWriter
from pdf_page_numbers import list_of_pdfs # Importing the list from another file
from pdf_names import pdf_names # Importing the list from another file
from pdf_categories import categories # Importing the list from another file
from pdf_article_levels import article_levels # Importing the list from another file
from pdf2image import convert_from_path



pdf_source_name = "English Digest_May 2025.pdf"
pdf_source_name = pdf_source_name.replace(".pdf", "")



# Creating sub-pdf from source pdf given the page ranges
def extract_pages(pdf_source_name_path, pdf_b_path, start_page, end_page):
    """
    Creates PDF B from PDF A given the page range [start_page, end_page] (1-based, inclusive).
    """
    reader = PdfReader("./sources/" + pdf_source_name_path.replace(".pdf", "") + ".pdf")
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
def create_dir():
    """Create directory for sub-pdfs creation"""
    if not os.path.exists(f'./extracted/{pdf_source_name}'):
        os.makedirs(f'./extracted/{pdf_source_name}')


# Main function to generate sub-pdf extractions
def generate_pdf_extractions():

    # Basic validation of pdfs lists and names
    if len(list_of_pdfs)-1 != len(pdf_names):
        print(f'Warning: The number of PDF files and names do not match: {len(list_of_pdfs)-1} != {len(pdf_names)}')
        exit(1)


    # Creating sub-pdfs from source pdf
    create_dir()
    print("extracting files...")
    
    order = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    for i in range(len(list_of_pdfs) - 1):
        if pdf_names[i] != "None" and pdf_names[i] != "none":
            new_pdf_name = f"{order[i]}_category" + "-" + pdf_names[i] + "-" + pdf_source_name + ' Level'
            new_pdf_name = new_pdf_name.title().replace("  ", " ").replace(" ", "_").replace(":", "").replace("’", "").replace("'", "").replace("&", "and")
            pdf_b = f"./extracted/{pdf_source_name}/{new_pdf_name}.pdf"
            start_page = list_of_pdfs[i]
            end_page = list_of_pdfs[i + 1]-1
            extract_pages(pdf_source_name, pdf_b, start_page, end_page)
            print(f"\t{new_pdf_name}")

    print("Extraction completed.")


     # Extracting text from each sub-pdf and saving to a .txt file

    print("Extracting text from pdfs using OCR...")

    #
    dict_of_pdf_texts = []

    import json

    for filename in sorted(os.listdir(f'./extracted/{pdf_source_name}')):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(f'./extracted/{pdf_source_name}', filename)
            dict_of_pdf_texts.append( json.dumps( { "title": filename, "text" : extract_text_from_pdf(pdf_path) }, indent=4 ) )
            # break

    # dict_of_pdf_texts = f'{{ "articles": {dict_of_pdf_texts} }}'

    with open(f'./extracted/{pdf_source_name}/extraction_log.txt', "w", encoding="utf-8") as text_file:
        prompt = f"""You are a helpful English assistant that helps to classify articles into categories and levels based on their content.
        please use the following rules or criteria for classifying articles. 
        Please return 2 arrays. 1. An array of categories names and 2. An array of levels.
        1. The categories should be determined by the article title matching to the following list: {categories}
        2. The levels of the articles should be determined by the article content. Consider the levels being 1, 1.5, 2, 3, 4. Consider the levels being for kids in Taiwan of grade 5, Junior high school 2, junior high school 3, Senior high school grade 1, senior high school grade 2 respectively. for example if the article contains simple vocabulary and sentence structure, let the level be 1. If the vocabulary and sentence structure are complex let it be level 4.

        Below is the data obtained from OCR extraction of articles containing their respective articles titles and the content of the articles:

        {dict_of_pdf_texts.__str__()}
        """
        # print(prompt)
        text_file.write(prompt)

    print(f"Extraction completed and saved to ./extracted/{pdf_source_name}/extraction_log.txt.")

    print("Please copy prompt from extraction_log.txt and paste it into chatGPT.com. Then return to paste the output.")



generate_pdf_extractions()