

import os
from PyPDF2 import PdfReader, PdfWriter


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


list_of_pdfs = [1, 4, 8, 9, 12, 21, 23, 25, 27, 29, 31, 32, 34, 
                37, 41, 42, 44, 46, 49, 52, 56, 58, 60,
                  62, 66, 67, 69, 75]

pdf_names = [
            "None",
            "Always on the move: Tuna’s No-Nap Lifestyle",
            "None",
            "Nine Minutes of Extra rest or Nine minutes of regret?",
            "None",
            "An Empire of Convenience: The story of 7-Eleven",
            "None",
            "Have a Finger in Every Pie",
            "The Secrets of Culinary Crowns",
            "None",
            "EU Approves Full Schengen Membership for Bulgaria and Romania",
            "Coffee Prices at a record High Due to Supply Shortage",
            "None",
            "Life on the International Space Station",
            "None",
            "The Psychology of Stockholm Syndrome",
            "None",
            "Welcome Gen Beta: AI-Driven Generation Takes the Stage",
            "Addressing a Canceled Reservation",
            "Riding Trains and Sipping Tea: Alishan’s Twin Treasures",
            "None",
            "Shower Shoes: Protecting Feet for Six Decades",
            "None",
            "2024's Words of the year: give new meaning to old terms",
            "None",
            "Gobekli Tepe: Rewriting history's first chapter",
            "None"
            ]

article_levels = [ 2, 2, 1.5, 1, 1.5, 2, 2, 2, 1.5, 2, 1.5, 1.5, 2, 1.5, 2 ]


categories = [
    "None",  # Empty
    "Animals & Pets",  # Always on the move: Tuna’s No-Nap Lifestyle
    "None",  # Empty
    "Time & Procastination",  # Nine Minutes of Extra rest or Nine minutes of regret?
    "None",  # Empty
    "Jobs & Business",  # An Empire of Convenience: The story of 7-Eleven
    "None",  # Empty
    "Food & drinks",  # Have a Finger in Every Pie
    "Food & drinks",  # The Secrets of Culinary Crowns
    "None",  # Empty
    "News & shows & celebrities",  # EU Approves Full Schengen Membership for Bulgaria and Romania
    "Shopping & Money",  # Coffee Prices at a record High Due to Supply Shortage
    "None",  # Empty
    "Technology",  # Life on the International Space Station
    "None",  # Empty
    "Self awareness & mental health",  # The Psychology of Stockholm Syndrome
    "None",  # Empty
    "Society & Trend",  # Welcome Gen Beta: AI-Driven Generation Takes the Stage
    "None",  # Empty
    "Communication & life skills",  # Addressing a Canceled Reservation
    "Travel",  # Riding Trains and Sipping Tea: Alishan’s Twin Treasures
    "None",  # Empty
    "Safety",  # Shower Shoes: Protecting Feet for Six Decades
    "None",  # Empty
    "Language",  # 2024's Words of the year: give new meaning to old terms
    "None",  # Empty
    "Study & History",  # Gobekli Tepe: Rewriting history's first chapter
    "None"  # Empty
]


pdf_source_name = "Analytical English _May 2025"
pdf_source_name = pdf_source_name.replace(".pdf", "")

def create_dir():
    if not os.path.exists(f'./extracted/{pdf_source_name}'):
        os.makedirs(f'./extracted/{pdf_source_name}')


def generate_pdf_extractions():
    if len(list_of_pdfs)-1 != len(pdf_names):
        print(f'Warning: The number of PDF files and names do not match: {len(list_of_pdfs)-1} != {len(pdf_names)}')
        exit(1)

    create_dir()

    print("extracting files...")
    for i in range(len(list_of_pdfs) - 1):
        if pdf_names[i] != "None":
            new_pdf_name = categories.pop(0) + "-" + pdf_names[i] + "-" + pdf_source_name + f' Level {article_levels.pop(0)}'
            new_pdf_name = new_pdf_name.title().replace("  ", " ").replace(" ", "_").replace(":", "").replace("’", "").replace("'", "").replace("&", "and")
            pdf_b = f"./extracted/{pdf_source_name}/{new_pdf_name}.pdf"
            start_page = list_of_pdfs[i]
            end_page = list_of_pdfs[i + 1]-1
            extract_pages(pdf_source_name, pdf_b, start_page, end_page)
            print(f"\t{new_pdf_name}")
        else:
            try:
                if categories[0] == "None":
                    categories.pop(0)
            except IndexError:
                pass

            try:
                if article_levels[0] == 0:
                    article_levels.pop(0)
            except IndexError:
                pass

    print("Extraction completed.")


generate_pdf_extractions()