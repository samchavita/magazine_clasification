import sys
import json
from clasify import generate_pdf_extractions

def main():
    data = sys.stdin.read()
    tuples = json.loads(data)  # [{ "page": 1, "title": "..." }, ...]\
    file = tuples.get("file")
    tuples = tuples.get("tuples")
    
    print(f"Received file: {file}")
    print(f"Received tuples: {tuples}")

    # for tup in tuples:
    #     print(f"Start Page: {tup['page']}, Title: {tup['title']}")
    if file and tuples:
        generate_pdf_extractions(file, tuples)
    else:
        print("Invalid input data. 'file' and 'tuples' are required.")

    # generate_pdf_extractions(tuples)

if __name__ == '__main__':
    main()
