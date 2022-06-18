import os
from tika import parser





def main():
    pdf_folder_path = r"C:\Users\noam.s\Desktop\important\money\cal"
    pdf_name = r"2020_10_.pdf"
    pdf_path = os.path.join(pdf_folder_path, pdf_name)

    raw = parser.from_file(pdf_path)
    print(raw["content"])
    pass


if __name__ == "__main__":
    main()