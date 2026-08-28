# 📇 Visiting Card Scanner

A Python-based **Visiting Card Scanner** that automatically extracts contact information from visiting/business card images using **Optical Character Recognition (OCR)**. The application provides a simple graphical interface where users can upload a card image, scan it, extract important details, preview the information, and save or export the data in multiple formats.

## 🚀 Features

* 📤 Upload visiting card images (`JPG`, `JPEG`, `PNG`)
* 🔍 Extract text from images using **Tesseract OCR**
* 👤 Identify basic contact details such as:

  * Name
  * Company
  * Job Title
  * Email
  * Phone Number
  * Website
  * Address
  * Raw OCR Text
* 🖼️ Preview the uploaded visiting card
* 📋 Display extracted card details in the application
* 📊 Generate CSV-formatted data
* 📁 Export contact information to CSV
* 📗 Save/update contact information in Excel
* 📄 Export individual card details as PDF
* 📂 Automatically create and manage a `Database` folder
* 🖥️ User-friendly desktop GUI using Tkinter

## 🛠️ Technologies Used

* **Python**
* **Tkinter** – Graphical User Interface
* **Tesseract OCR** – Text recognition from images
* **Pytesseract** – Python wrapper for Tesseract OCR
* **Pillow (PIL)** – Image processing and preview
* **Regular Expressions (Regex)** – Extraction of email, phone number, and website
* **Pandas** – CSV and Excel data management
* **FPDF** – PDF generation

## ⚙️ How It Works

1. Upload a visiting card image.
2. The application displays the selected image.
3. Click **Scan Card** to perform OCR using Tesseract.
4. The extracted text is processed using regular expressions and basic parsing logic.
5. Contact information is organized into structured fields.
6. Users can preview the extracted details.
7. The information can be exported as:

   * CSV
   * Excel
   * PDF
8. All generated files are stored inside the `Database` folder.

## 📂 Project Structure

```text
Visiting-Card-Scanner/
│
├── main.py
├── Database/
│   ├── exported_data.csv
│   ├── exported_data.xlsx
│   └── Card_Name.pdf
│
└── README.md
```

## 📦 Installation

Install the required Python libraries:

```bash
pip install pillow pytesseract pandas fpdf
```

You also need to install **Tesseract OCR** on your system.

After installing Tesseract, update the Tesseract executable path in `main.py` if required.

## ▶️ Run the Application

```bash
python main.py
```

The application will open a desktop window where you can upload and scan visiting cards.

## 💡 Use Cases

* Digitizing business cards
* Maintaining customer contact information
* Building a personal contact database
* Reducing manual data entry
* Organizing professional networking contacts
* Converting physical business cards into digital records

## 🔮 Future Enhancements

* Improve name, company, and address detection using NLP
* Support multiple visiting cards at once
* Add database integration using MySQL or SQLite
* Add duplicate-contact detection
* Support additional languages
* Improve OCR accuracy with image preprocessing
* Add search and filter functionality
* Add cloud-based contact synchronization

## 👩‍💻 Project

**Visiting Card Scanner – OCR-Based Contact Information Extraction**

This project demonstrates the integration of **Python GUI development, OCR, image processing, regular expressions, and data management** to automate the process of converting visiting card information into structured digital data.
