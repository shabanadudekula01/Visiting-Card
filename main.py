import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import pytesseract
import os
import re
import csv
import pandas as pd # type: ignore
from fpdf import FPDF # type: ignore

# Setup Tesseract Path - Adjust if installed elsewhere
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Setup Database folder
if not os.path.exists('Database'):
    os.makedirs('Database')

class VisitingCardScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Visiting Card Scanner")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        self.filename = None
        self.extracted_text = ""
        self.extracted_data = {}
        
        self.create_menu()
        self.create_layout()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=lambda: messagebox.showinfo("About", "Visiting Card Scanner\nDeveloper: Kartik Mathur"))
        menubar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menubar)

    def create_layout(self):
        # 1. Header Section
        header_frame = tk.Frame(self.root, bg="#f5deb3", pady=10) # Peach/orange background
        header_frame.pack(side=tk.TOP, fill=tk.X)
        
        tk.Label(header_frame, text="Visiting Card Scanner", font=("Times New Roman", 24, "bold"), bg="#f5deb3", fg="#333333").pack()
        tk.Label(header_frame, text="Upload, scan, display, save, and export card details", font=("Times New Roman", 14, "italic"), bg="#f5deb3", fg="#555555").pack()

        # Main Paned Window
        main_pane = tk.PanedWindow(self.root, orient=tk.VERTICAL, sashwidth=5)
        main_pane.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 2. Middle Section (Left & Right)
        middle_frame = tk.Frame(main_pane)
        main_pane.add(middle_frame, stretch="always")
        
        # Left Panel (Buttons)
        left_panel = tk.Frame(middle_frame, width=200, relief=tk.SUNKEN, borderwidth=1, bg="#e0e0e0", padx=10, pady=10)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Button styles (approximating the image colors)
        btn_font = ("Arial", 11, "bold")
        
        btn_configs = [
            ("Upload Card", "#ed7d31", "white", self.upload_card),
            ("Scan Card", "#5b9bd5", "white", self.scan_card),
            ("Display Details", "#70ad47", "white", self.display_details),
            ("Generate CSV Data", "#ffc000", "black", self.generate_csv),
            ("Save/Update Excel", "#00a29a", "white", self.save_excel),
            ("Export CSV", "#9933ff", "white", self.export_csv),
            ("Export PDF", "#c55a11", "white", self.export_pdf),
            ("Open Data Folder", "#a5a5a5", "black", self.open_folder),
        ]
        
        for text, bg, fg, cmd in btn_configs:
            btn = tk.Button(left_panel, text=text, bg=bg, fg=fg, font=btn_font, width=20, command=cmd)
            btn.pack(pady=5)

        # Right Panel (Image Preview)
        right_panel = tk.Frame(middle_frame, relief=tk.SUNKEN, borderwidth=1, bg="#f0f0f0")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        tk.Label(right_panel, text="Selected Image Preview", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=10)
        
        self.image_label = tk.Label(right_panel, bg="#f0f0f0")
        self.image_label.pack(expand=True, fill=tk.BOTH)

        # 3. Bottom Section (Output text)
        bottom_frame = tk.Frame(main_pane, relief=tk.SUNKEN, borderwidth=1)
        main_pane.add(bottom_frame, stretch="never", height=150)
        
        tk.Label(bottom_frame, text="Output / CSV Preview", font=("Arial", 12, "bold"), anchor="w").pack(fill=tk.X, padx=5, pady=2)
        
        self.output_text = scrolledtext.ScrolledText(bottom_frame, height=5, font=("Courier", 10), bg="#f5f5f5")
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.output_text.insert(tk.END, "Name,Company,Title,Email,Phone,Website,Address,RawText\n")

    def upload_card(self):
        self.filename = filedialog.askopenfilename(
            initialdir='/Desktop', title='Select a card image',
            filetypes=(('Image files', '*.jpg *.jpeg *.png'), ('All files', '*.*')))
        
        if self.filename:
            try:
                img = Image.open(self.filename)
                # Resize image to fit preview while maintaining aspect ratio
                img.thumbnail((500, 400))
                self.photo = ImageTk.PhotoImage(img)
                self.image_label.config(image=self.photo)
                self.output_text.insert(tk.END, f"\n[System] Image loaded: {self.filename}\n")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image.\n{e}")

    def scan_card(self):
        if not self.filename:
            messagebox.showwarning("Warning", "Please upload an image first.")
            return
            
        try:
            self.output_text.insert(tk.END, "\n[System] Scanning image...\n")
            self.root.update()
            self.extracted_text = pytesseract.image_to_string(self.filename)
            self.output_text.insert(tk.END, "[System] Scan Complete. Raw Text:\n")
            self.output_text.insert(tk.END, f"{self.extracted_text}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Tesseract error.\n{e}\nEnsure Tesseract OCR is installed.")

    def display_details(self):
        # Displays the parsed details in a neat format
        if not self.extracted_text:
            messagebox.showwarning("Warning", "Please scan a card first.")
            return
        self.parse_data()
        
        details = "\n--- Card Details ---\n"
        for k, v in self.extracted_data.items():
            if k != "RawText":
                details += f"{k}: {v}\n"
        details += "--------------------\n"
        self.output_text.insert(tk.END, details)

    def parse_data(self):
        # Basic Regex parsing logic for visiting card details
        text = self.extracted_text
        
        email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
        phone_pattern = r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]'
        url_pattern = r'(www\.[^\s]+|[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(/\S*)?)'
        
        email = re.search(email_pattern, text)
        phone = re.search(phone_pattern, text)
        website = re.search(url_pattern, text)
        
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        name = lines[0] if lines else ""
        title = lines[1] if len(lines) > 1 else ""
        company = lines[2] if len(lines) > 2 else "" # Guessing company
        
        self.extracted_data = {
            "Name": name,
            "Company": company,
            "Title": title,
            "Email": email.group(0) if email else "",
            "Phone": phone.group(0) if phone else "",
            "Website": website.group(0) if website else "",
            "Address": "", # Address parsing requires complex NLP, leaving blank for simple regex
            "RawText": text.replace('\n', ' ').strip()
        }

    def generate_csv(self):
        if not self.extracted_text:
            messagebox.showwarning("Warning", "Please scan a card first.")
            return
        
        self.parse_data()
        
        # Format as CSV row
        headers = ["Name", "Company", "Title", "Email", "Phone", "Website", "Address", "RawText"]
        row = [f'"{self.extracted_data.get(h, "")}"' for h in headers]
        csv_str = ",".join(row)
        
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "Name,Company,Title,Email,Phone,Website,Address,RawText\n")
        self.output_text.insert(tk.END, csv_str + "\n")

    def export_csv(self):
        if not self.extracted_data:
            self.generate_csv()
            if not self.extracted_data: return
            
        try:
            filepath = os.path.join("Database", "exported_data.csv")
            df = pd.DataFrame([self.extracted_data])
            df.to_csv(filepath, mode='a', header=not os.path.exists(filepath), index=False)
            messagebox.showinfo("Success", f"CSV Exported to {filepath}")
            self.output_text.insert(tk.END, f"\n[System] Appended to CSV: {filepath}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export CSV.\n{e}")

    def save_excel(self):
        if not self.extracted_data:
            self.generate_csv()
            if not self.extracted_data: return
            
        try:
            filepath = os.path.join("Database", "exported_data.xlsx")
            df = pd.DataFrame([self.extracted_data])
            if os.path.exists(filepath):
                with pd.ExcelWriter(filepath, mode='a', if_sheet_exists='overlay') as writer:
                    df.to_excel(writer, startrow=writer.sheets['Sheet1'].max_row, index=False, header=False)
            else:
                df.to_excel(filepath, index=False)
            messagebox.showinfo("Success", f"Excel saved/updated at {filepath}")
            self.output_text.insert(tk.END, f"\n[System] Appended to Excel: {filepath}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save Excel.\n{e}")

    def export_pdf(self):
        if not self.extracted_data:
            self.generate_csv()
            if not self.extracted_data: return
            
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Visiting Card Details", ln=1, align='C')
            
            for k, v in self.extracted_data.items():
                if k != "RawText":
                    # Fix fpdf unicode issues by encoding to latin-1 and ignoring errors
                    safe_txt = f"{k}: {v}".encode('latin-1', 'ignore').decode('latin-1')
                    pdf.cell(200, 10, txt=safe_txt, ln=1)
            
            filepath = os.path.join("Database", f"{self.extracted_data.get('Name', 'Card').replace(' ', '_')}.pdf")
            pdf.output(filepath)
            messagebox.showinfo("Success", f"PDF Exported to {filepath}")
            self.output_text.insert(tk.END, f"\n[System] Exported to PDF: {filepath}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export PDF.\n{e}")

    def open_folder(self):
        try:
            db_path = os.path.abspath("Database")
            os.startfile(db_path)
            self.output_text.insert(tk.END, f"\n[System] Opened Data Folder: {db_path}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open folder.\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VisitingCardScannerApp(root)
    root.mainloop()