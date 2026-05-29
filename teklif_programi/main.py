import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import sqlite3
import os
import sys
import traceback
from quotation_manager import QuotationManager
from company_manager import CompanyManager
from export_manager import ExportManager

class TeklifProgrami:
    def __init__(self, root):
        self.root = root
        self.root.title("MEFE Makina - Teklif Programı")
        self.root.geometry("1200x800")
        
        # Set database path to user-writable location (AppData)
        if getattr(sys, 'frozen', False):
            # Running as executable
            app_data = os.path.expandvars('%APPDATA%')
            self.db_path = os.path.join(app_data, 'MEFE_Makina_Teklif')
        else:
            # Running as script
            self.db_path = os.path.dirname(os.path.abspath(__file__))
        
        # Create database directory if it doesn't exist
        if not os.path.exists(self.db_path):
            os.makedirs(self.db_path)
        
        # Initialize managers
        self.quotation_manager = QuotationManager(self.db_path)
        self.company_manager = CompanyManager(self.db_path)
        self.export_manager = ExportManager()
        
        # Create main interface
        self.create_main_interface()
        
    def create_main_interface(self):
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_quotation_tab()
        self.create_company_tab()
        self.create_history_tab()
        
    def create_quotation_tab(self):
        self.quotation_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.quotation_frame, text="Yeni Teklif")
        
        # Main container
        main_container = ttk.Frame(self.quotation_frame)
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Header section
        header_frame = ttk.LabelFrame(main_container, text="Teklif Bilgileri")
        header_frame.pack(fill='x', padx=5, pady=5)
        
        # Quotation number
        ttk.Label(header_frame, text="Teklif No:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.quotation_no_var = tk.StringVar()
        self.quotation_no_entry = ttk.Entry(header_frame, textvariable=self.quotation_no_var, state='readonly')
        self.quotation_no_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        
        # Date
        ttk.Label(header_frame, text="Tarih:").grid(row=0, column=2, padx=5, pady=5, sticky='e')
        self.date_var = tk.StringVar(value=datetime.now().strftime("%d.%m.%Y"))
        ttk.Entry(header_frame, textvariable=self.date_var).grid(row=0, column=3, padx=5, pady=5, sticky='w')
        
        # Company selection
        ttk.Label(header_frame, text="Firma:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.company_var = tk.StringVar()
        self.company_combo = ttk.Combobox(header_frame, textvariable=self.company_var, state='readonly')
        self.company_combo.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.load_companies()
        
        ttk.Button(header_frame, text="Yeni Firma", command=self.open_company_dialog).grid(row=1, column=2, padx=5, pady=5)
        
        # Delivery type
        ttk.Label(header_frame, text="Teslimat Tipi:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.delivery_type_var = tk.StringVar()
        delivery_types = ["Yurt İçi", "Yurt Dışı", "DAP", "DDP", "EXW", "FOB", "CIF"]
        ttk.Combobox(header_frame, textvariable=self.delivery_type_var, values=delivery_types, state='readonly').grid(row=2, column=1, padx=5, pady=5, sticky='w')
        
        # Currency
        ttk.Label(header_frame, text="Para Birimi:").grid(row=2, column=2, padx=5, pady=5, sticky='e')
        self.currency_var = tk.StringVar(value="TL")
        currencies = ["TL", "USD", "EUR"]
        ttk.Combobox(header_frame, textvariable=self.currency_var, values=currencies, state='readonly').grid(row=2, column=3, padx=5, pady=5, sticky='w')
        
        # Items section
        items_frame = ttk.LabelFrame(main_container, text="Kalemler")
        items_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Items table
        columns = ("Sıra", "Kod", "Açıklama", "Miktar", "Birim", "Birim Fiyat", "Toplam")
        self.items_tree = ttk.Treeview(items_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.items_tree.heading(col, text=col)
            self.items_tree.column(col, width=100)
        
        self.items_tree.column("Açıklama", width=200)
        self.items_tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Item input section
        input_frame = ttk.Frame(items_frame)
        input_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(input_frame, text="Kod:").grid(row=0, column=0, padx=5, pady=5)
        self.item_code_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.item_code_var, width=15).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Açıklama:").grid(row=0, column=2, padx=5, pady=5)
        self.item_desc_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.item_desc_var, width=30).grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Miktar:").grid(row=0, column=4, padx=5, pady=5)
        self.item_qty_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.item_qty_var, width=10).grid(row=0, column=5, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Birim:").grid(row=0, column=6, padx=5, pady=5)
        self.item_unit_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.item_unit_var, width=10).grid(row=0, column=7, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Birim Fiyat:").grid(row=0, column=8, padx=5, pady=5)
        self.item_price_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.item_price_var, width=15).grid(row=0, column=9, padx=5, pady=5)
        
        ttk.Button(input_frame, text="Ekle", command=self.add_item).grid(row=0, column=10, padx=5, pady=5)
        ttk.Button(input_frame, text="Sil", command=self.remove_item).grid(row=0, column=11, padx=5, pady=5)
        
        # Notes section
        notes_frame = ttk.LabelFrame(main_container, text="Notlar")
        notes_frame.pack(fill='x', padx=5, pady=5)
        
        self.notes_text = tk.Text(notes_frame, height=5)
        self.notes_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(main_container)
        button_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(button_frame, text="Teklif No Oluştur", command=self.generate_quotation_no).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Kaydet", command=self.save_quotation).pack(side='left', padx=5)
        ttk.Button(button_frame, text="PDF Dışa Aktar", command=self.export_pdf).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Excel Dışa Aktar", command=self.export_excel).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Temizle", command=self.clear_form).pack(side='left', padx=5)
        
        # Generate initial quotation number
        self.generate_quotation_no()
        
    def create_company_tab(self):
        self.company_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.company_frame, text="Firma Yönetimi")
        
        # Company list
        list_frame = ttk.LabelFrame(self.company_frame, text="Firmalar")
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ("ID", "Firma Adı", "Vergi No", "Telefon", "E-posta", "Adres")
        self.company_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        for col in columns:
            self.company_tree.heading(col, text=col)
            self.company_tree.column(col, width=120)
        
        self.company_tree.column("Adres", width=200)
        self.company_tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(self.company_frame)
        button_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(button_frame, text="Yeni Firma", command=self.open_company_dialog).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Düzenle", command=self.edit_company).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Sil", command=self.delete_company).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Yenile", command=self.load_companies_to_tree).pack(side='left', padx=5)
        
        self.load_companies_to_tree()
        
    def create_history_tab(self):
        self.history_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.history_frame, text="Teklif Geçmişi")
        
        # History list
        list_frame = ttk.LabelFrame(self.history_frame, text="Teklifler")
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ("Teklif No", "Tarih", "Firma", "Teslimat", "Para Birimi", "Toplam Tutar")
        self.history_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        for col in columns:
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=120)
        
        self.history_tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(self.history_frame)
        button_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(button_frame, text="Yenile", command=self.load_history).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Görüntüle", command=self.view_quotation).pack(side='left', padx=5)
        
        self.load_history()
        
    def generate_quotation_no(self):
        quotation_no = self.quotation_manager.generate_quotation_no()
        self.quotation_no_var.set(quotation_no)
        
    def load_companies(self):
        companies = self.company_manager.get_all_companies()
        company_names = [c[1] for c in companies]
        self.company_combo['values'] = company_names
        
    def load_companies_to_tree(self):
        self.company_tree.delete(*self.company_tree.get_children())
        companies = self.company_manager.get_all_companies()
        for company in companies:
            self.company_tree.insert('', 'end', values=company)
            
    def load_history(self):
        self.history_tree.delete(*self.history_tree.get_children())
        quotations = self.quotation_manager.get_all_quotations()
        for quotation in quotations:
            self.history_tree.insert('', 'end', values=quotation)
            
    def add_item(self):
        try:
            code = self.item_code_var.get()
            description = self.item_desc_var.get()
            quantity = float(self.item_qty_var.get())
            unit = self.item_unit_var.get()
            price = float(self.item_price_var.get())
            total = quantity * price
            
            items = self.items_tree.get_children()
            seq = len(items) + 1
            
            self.items_tree.insert('', 'end', values=(seq, code, description, quantity, unit, price, total))
            
            # Clear inputs
            self.item_code_var.set('')
            self.item_desc_var.set('')
            self.item_qty_var.set('')
            self.item_unit_var.set('')
            self.item_price_var.set('')
            
        except ValueError:
            messagebox.showerror("Hata", "Lütfen geçerli sayısal değerler girin.")
            
    def remove_item(self):
        selected = self.items_tree.selection()
        if selected:
            self.items_tree.delete(selected)
            # Update sequence numbers
            for idx, item in enumerate(self.items_tree.get_children(), 1):
                values = list(self.items_tree.item(item)['values'])
                values[0] = idx
                self.items_tree.item(item, values=values)
                
    def open_company_dialog(self, company_id=None):
        dialog = tk.Toplevel(self.root)
        dialog.title("Firma")
        dialog.geometry("500x400")
        
        ttk.Label(dialog, text="Firma Adı:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        name_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=name_var, width=40).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Vergi No:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        tax_no_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=tax_no_var, width=40).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Telefon:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        phone_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=phone_var, width=40).grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="E-posta:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        email_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=email_var, width=40).grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Adres:").grid(row=4, column=0, padx=5, pady=5, sticky='e')
        address_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=address_var, width=40).grid(row=4, column=1, padx=5, pady=5)
        
        def save():
            name = name_var.get()
            tax_no = tax_no_var.get()
            phone = phone_var.get()
            email = email_var.get()
            address = address_var.get()
            
            if not name:
                messagebox.showerror("Hata", "Firma adı zorunludur.")
                return
                
            self.company_manager.add_company(name, tax_no, phone, email, address)
            self.load_companies()
            self.load_companies_to_tree()
            dialog.destroy()
            
        ttk.Button(dialog, text="Kaydet", command=save).grid(row=5, column=0, columnspan=2, pady=20)
        
        # If editing, load existing data
        if company_id:
            company = self.company_manager.get_company(company_id)
            if company:
                name_var.set(company[1])
                tax_no_var.set(company[2])
                phone_var.set(company[3])
                email_var.set(company[4])
                address_var.set(company[5])
                
    def edit_company(self):
        selected = self.company_tree.selection()
        if selected:
            company_id = self.company_tree.item(selected[0])['values'][0]
            self.open_company_dialog(company_id)
            
    def delete_company(self):
        selected = self.company_tree.selection()
        if selected:
            if messagebox.askyesno("Onay", "Bu firmayı silmek istediğinizden emin misiniz?"):
                company_id = self.company_tree.item(selected[0])['values'][0]
                self.company_manager.delete_company(company_id)
                self.load_companies()
                self.load_companies_to_tree()
                
    def save_quotation(self):
        try:
            quotation_no = self.quotation_no_var.get()
            date = self.date_var.get()
            company_name = self.company_var.get()
            delivery_type = self.delivery_type_var.get()
            currency = self.currency_var.get()
            notes = self.notes_text.get("1.0", tk.END).strip()
            
            if not company_name:
                messagebox.showerror("Hata", "Firma seçiniz.")
                return
                
            if not delivery_type:
                messagebox.showerror("Hata", "Teslimat tipi seçiniz.")
                return
                
            # Get items
            items = []
            total_amount = 0
            for item in self.items_tree.get_children():
                values = self.items_tree.item(item)['values']
                items.append({
                    'code': values[1],
                    'description': values[2],
                    'quantity': values[3],
                    'unit': values[4],
                    'unit_price': values[5],
                    'total': values[6]
                })
                total_amount += float(values[6])
                
            if not items:
                messagebox.showerror("Hata", "En az bir kalem ekleyiniz.")
                return
                
            # Get company ID
            company_id = self.company_manager.get_company_id_by_name(company_name)
            
            # Save quotation
            self.quotation_manager.add_quotation(
                quotation_no, date, company_id, delivery_type, 
                currency, total_amount, notes, items
            )
            
            messagebox.showinfo("Başarılı", "Teklif başarıyla kaydedildi.")
            self.load_history()
            self.clear_form()
        except Exception as e:
            error_msg = f"Teklif kaydetme hatası:\n{str(e)}\n\nDetaylar:\n{traceback.format_exc()}"
            messagebox.showerror("Hata", error_msg)
        
    def clear_form(self):
        self.generate_quotation_no()
        self.date_var.set(datetime.now().strftime("%d.%m.%Y"))
        self.company_var.set('')
        self.delivery_type_var.set('')
        self.currency_var.set('TL')
        self.items_tree.delete(*self.items_tree.get_children())
        self.notes_text.delete("1.0", tk.END)
        
    def export_pdf(self):
        try:
            quotation_no = self.quotation_no_var.get()
            company_name = self.company_var.get()
            delivery_type = self.delivery_type_var.get()
            currency = self.currency_var.get()
            notes = self.notes_text.get("1.0", tk.END).strip()
            
            if not company_name:
                messagebox.showerror("Hata", "Firma seçiniz.")
                return
                
            if not delivery_type:
                messagebox.showerror("Hata", "Teslimat tipi seçiniz.")
                return
                
            # Get items from form
            items = []
            total_amount = 0
            for item in self.items_tree.get_children():
                values = self.items_tree.item(item)['values']
                items.append({
                    'code': values[1],
                    'description': values[2],
                    'quantity': values[3],
                    'unit': values[4],
                    'unit_price': values[5],
                    'total': values[6]
                })
                total_amount += float(values[6])
                
            if not items:
                messagebox.showerror("Hata", "En az bir kalem ekleyiniz.")
                return
                
            file_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                initialfile=f"{quotation_no}.pdf"
            )
            
            if file_path:
                quotation = {
                    'quotation_no': quotation_no,
                    'date': self.date_var.get(),
                    'company_id': None,
                    'company_name': company_name,
                    'delivery_type': delivery_type,
                    'currency': currency,
                    'total_amount': total_amount,
                    'notes': notes,
                    'items': items
                }
                self.export_manager.export_pdf(quotation, file_path)
                messagebox.showinfo("Başarılı", "PDF başarıyla dışa aktarıldı.")
                # Auto-open PDF
                os.startfile(file_path)
        except Exception as e:
            error_msg = f"PDF dışa aktarma hatası:\n{str(e)}\n\nDetaylar:\n{traceback.format_exc()}"
            messagebox.showerror("Hata", error_msg)
                
    def export_excel(self):
        quotation_no = self.quotation_no_var.get()
        company_name = self.company_var.get()
        delivery_type = self.delivery_type_var.get()
        currency = self.currency_var.get()
        notes = self.notes_text.get("1.0", tk.END).strip()
        
        if not company_name:
            messagebox.showerror("Hata", "Firma seçiniz.")
            return
            
        if not delivery_type:
            messagebox.showerror("Hata", "Teslimat tipi seçiniz.")
            return
            
        # Get items from form
        items = []
        total_amount = 0
        for item in self.items_tree.get_children():
            values = self.items_tree.item(item)['values']
            items.append({
                'code': values[1],
                'description': values[2],
                'quantity': values[3],
                'unit': values[4],
                'unit_price': values[5],
                'total': values[6]
            })
            total_amount += float(values[6])
            
        if not items:
            messagebox.showerror("Hata", "En az bir kalem ekleyiniz.")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            initialfile=f"{quotation_no}.xlsx"
        )
        
        if file_path:
            quotation = {
                'quotation_no': quotation_no,
                'date': self.date_var.get(),
                'company_id': None,
                'delivery_type': delivery_type,
                'currency': currency,
                'total_amount': total_amount,
                'notes': notes,
                'items': items
            }
            try:
                self.export_manager.export_excel(quotation, file_path)
                messagebox.showinfo("Başarılı", "Excel başarıyla dışa aktarıldı.")
                # Auto-open Excel
                os.startfile(file_path)
            except Exception as e:
                messagebox.showerror("Hata", f"Excel oluşturulurken hata: {str(e)}")
                
    def view_quotation(self):
        selected = self.history_tree.selection()
        if selected:
            quotation_no = self.history_tree.item(selected[0])['values'][0]
            quotation = self.quotation_manager.get_quotation_by_no(quotation_no)
            if quotation:
                # Load quotation data to form
                self.quotation_no_var.set(quotation['quotation_no'])
                self.date_var.set(quotation['date'])
                company = self.company_manager.get_company(quotation['company_id'])
                if company:
                    self.company_var.set(company[1])
                self.delivery_type_var.set(quotation['delivery_type'])
                self.currency_var.set(quotation['currency'])
                self.notes_text.delete("1.0", tk.END)
                self.notes_text.insert("1.0", quotation['notes'])
                
                # Load items
                self.items_tree.delete(*self.items_tree.get_children())
                for idx, item in enumerate(quotation['items'], 1):
                    self.items_tree.insert('', 'end', values=(
                        idx, item['code'], item['description'], 
                        item['quantity'], item['unit'], 
                        item['unit_price'], item['total']
                    ))
                
                self.notebook.select(0)

if __name__ == "__main__":
    root = tk.Tk()
    app = TeklifProgrami(root)
    root.mainloop()
