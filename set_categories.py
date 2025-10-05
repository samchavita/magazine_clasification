import sys
import json
import os

def main():
    # Read input from stdin
    input_data = sys.stdin.read()
    data = json.loads(input_data)

    print("Data received in set_categories.py:" + str(data))

    categories = data.get("categories")
    file = data.get("file")

    print("in set_categories.py")
    print(f"Categories to set: {categories}")
    print(f"File: {file}")

    # read directory and get all .pdf files
    pdf_files = [f for f in os.listdir(f'./{file}') if f.endswith('.pdf')]
    pdf_files.sort()  # Sort files to maintain order

    print(f"PDF files found: {pdf_files}")
    if len(categories) != len(pdf_files):
        print(f"Error: The number of categories ({len(categories)}) does not match the number of PDF files ({len(pdf_files)}).")
        sys.exit(1)

    else:

        # rename files to include category
        try:
            for pdf, cat in zip(pdf_files, categories):
                base, ext = os.path.splitext(pdf)

                try:
                    base = '-'.join(base.split('-')[1:])  # Join all parts except the first
                except IndexError:
                    continue

                new_name = f"{cat.title().replace(' ', '_')}-{base}{ext}".replace('_-', '-').replace('--', '-')
                os.rename(os.path.join(f'./{file}', pdf), os.path.join(f'./{file}', new_name))
                print(f"Renamed: {pdf} -> {new_name}")
        except Exception as e:
            print(f"Error renaming files: {e}")
            sys.exit(1)
        print("All files renamed successfully.")
        

if __name__ == '__main__':
    main()

