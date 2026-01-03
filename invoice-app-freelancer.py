import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from fpdf import FPDF

class InvoiceGenerator(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Invoice / PDF Generator")
        self.geometry("850x650")
        self.resizable(False, False)

        self.items = []
        self.create_widgets()

    def create_widgets(self):
        container = ttk.Frame(self, padding=20)
        container.pack(fill='both', expand=True)

        title = ttk.Label(container, text="Invoice Generator", font=("Helvetica", 18, "bold"))
        title.pack(pady=(0, 15))

        # --- Info Section ---
        info_frame = ttk.Frame(container)
        info_frame.pack(fill='x', pady=(0, 15))

        left_info = ttk.Frame(info_frame)
        left_info.pack(side='left', expand=True, fill='x')

        right_info = ttk.Frame(info_frame)
        right_info.pack(side='left', expand=True, fill='x', padx=(20, 0))

        self.seller_name_var = tk.StringVar(value="")
        self.buyer_name_var = tk.StringVar(value="")
        self.invoice_no_var = tk.StringVar(value=datetime.now().strftime("%Y%m%d%H%M%S"))

        ttk.Label(left_info, text="Seller Name:").grid(row=0, column=0, sticky='w', pady=2)
        ttk.Entry(left_info, textvariable=self.seller_name_var, width=25).grid(row=0, column=1, padx=5)

        ttk.Label(left_info, text="Buyer Name:").grid(row=1, column=0, sticky='w', pady=2)
        ttk.Entry(left_info, textvariable=self.buyer_name_var, width=25).grid(row=1, column=1, padx=5)

        ttk.Label(left_info, text="Invoice No:").grid(row=2, column=0, sticky='w', pady=2)
        ttk.Entry(left_info, textvariable=self.invoice_no_var, width=25).grid(row=2, column=1, padx=5)

        self.seller_email_var = tk.StringVar(value="")
        self.buyer_email_var = tk.StringVar(value="")
        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))

        ttk.Label(right_info, text="Seller Email:").grid(row=0, column=0, sticky='w', pady=2)
        ttk.Entry(right_info, textvariable=self.seller_email_var, width=25).grid(row=0, column=1, padx=5)

        ttk.Label(right_info, text="Buyer Email:").grid(row=1, column=0, sticky='w', pady=2)
        ttk.Entry(right_info, textvariable=self.buyer_email_var, width=25).grid(row=1, column=1, padx=5)

        ttk.Label(right_info, text="Date:").grid(row=2, column=0, sticky='w', pady=2)
        ttk.Entry(right_info, textvariable=self.date_var, width=25).grid(row=2, column=1, padx=5)

        # --- Items Section ---
        items_frame = ttk.LabelFrame(container, text="Items", padding=10)
        items_frame.pack(fill='both', expand=True)

        header_frame = ttk.Frame(items_frame)
        header_frame.pack(fill='x', pady=(0, 5))

        ttk.Label(header_frame, text="Description", width=45, anchor='w').grid(row=0, column=0)
        ttk.Label(header_frame, text="Qty", width=8, anchor='center').grid(row=0, column=1, padx=5)
        ttk.Label(header_frame, text="Rate", width=10, anchor='center').grid(row=0, column=2, padx=5)
        ttk.Label(header_frame, text="Amount", width=12, anchor='center').grid(row=0, column=3, padx=5)
        ttk.Label(header_frame, text="", width=10).grid(row=0, column=4)

        self.items_container = ttk.Frame(items_frame)
        self.items_container.pack(fill='both', expand=True)

        # --- Totals Section ---
        totals_frame = ttk.Frame(container)
        totals_frame.pack(fill='x', pady=(10, 5))

        self.lbl_subtotal = ttk.Label(totals_frame, text="Subtotal: 0.00", font=("Helvetica", 10, "bold"))
        self.lbl_subtotal.pack(side='left', padx=(0, 20))

        self.lbl_tax = ttk.Label(totals_frame, text="Tax: 0.00", font=("Helvetica", 10, "bold"))
        self.lbl_tax.pack(side='left', padx=(0, 20))

        self.lbl_total = ttk.Label(totals_frame, text="Total: 0.00", font=("Helvetica", 10, "bold"))
        self.lbl_total.pack(side='left')

        # --- Options Section ---
        options_frame = ttk.Frame(container)
        options_frame.pack(fill='x', pady=(10, 10))

        ttk.Label(options_frame, text="Tax %:").pack(side='left')
        self.tax_var = tk.DoubleVar(value=0.0)
        tax_entry = ttk.Entry(options_frame, textvariable=self.tax_var, width=7)
        tax_entry.pack(side='left', padx=5)
        tax_entry.bind("<KeyRelease>", lambda e: self.update_totals())

        ttk.Label(options_frame, text="Currency:").pack(side='left', padx=(15, 5))
        self.currency_var = tk.StringVar(value="USD")
        currency_box = ttk.Combobox(options_frame, textvariable=self.currency_var, values=["USD", "EUR", "GBP", "INR"], width=5, state="readonly")
        currency_box.pack(side='left')

        ttk.Label(options_frame, text="Filename:").pack(side='left', padx=(15, 5))
        self.filename_var = tk.StringVar(value=f"invoice_{self.invoice_no_var.get()}.pdf")
        ttk.Entry(options_frame, textvariable=self.filename_var, width=30).pack(side='left')

        save_btn = ttk.Button(options_frame, text="Save PDF", command=self.save_pdf)
        save_btn.pack(side='right', padx=10, ipadx=10, ipady=5)

        # Add Item button (AFTER all variables are initialized)
        add_btn = ttk.Button(items_frame, text="Add Item", command=self.add_item)
        add_btn.pack(anchor='w', pady=(10, 0))

        # Notes section
        notes_frame = ttk.LabelFrame(container, text="Notes", padding=10)
        notes_frame.pack(fill='both', expand=True, pady=(15, 0))

        self.notes_text = tk.Text(notes_frame, height=5)
        self.notes_text.pack(fill='both', expand=True)
        self.notes_text.insert('1.0', "Thanks for your business!")

        # Add first item AFTER tax_var and totals are defined
        self.add_item()

    def add_item(self):
        item_frame = ttk.Frame(self.items_container)
        item_frame.pack(fill='x', pady=2)

        desc_var = tk.StringVar(value="Item Description")
        qty_var = tk.IntVar(value=1)
        rate_var = tk.DoubleVar(value=0.0)
        amount_var = tk.StringVar(value="0.00")

        ttk.Entry(item_frame, textvariable=desc_var, width=45).grid(row=0, column=0, sticky='w')
        qty_entry = ttk.Entry(item_frame, textvariable=qty_var, width=8, justify='center')
        qty_entry.grid(row=0, column=1, padx=5)
        qty_entry.bind("<KeyRelease>", lambda e: self.update_totals())

        rate_entry = ttk.Entry(item_frame, textvariable=rate_var, width=10, justify='center')
        rate_entry.grid(row=0, column=2, padx=5)
        rate_entry.bind("<KeyRelease>", lambda e: self.update_totals())

        ttk.Label(item_frame, textvariable=amount_var, width=12, anchor='center', relief='sunken').grid(row=0, column=3, padx=5)

        ttk.Button(item_frame, text="Remove", width=8, command=lambda: self.remove_item(item_frame)).grid(row=0, column=4, padx=5)

        self.items.append({
            "frame": item_frame,
            "desc": desc_var,
            "qty": qty_var,
            "rate": rate_var,
            "amount": amount_var,
        })

        self.update_totals()

    def remove_item(self, frame):
        for item in self.items:
            if item["frame"] == frame:
                self.items.remove(item)
                break
        frame.destroy()
        self.update_totals()

    def update_totals(self):
        subtotal = 0.0
        for item in self.items:
            try:
                qty = item["qty"].get()
                rate = item["rate"].get()
                amount = qty * rate
                item["amount"].set(f"{amount:.2f}")
                subtotal += amount
            except Exception:
                item["amount"].set("0.00")

        self.lbl_subtotal.config(text=f"Subtotal: {subtotal:.2f}")

        try:
            tax_percent = self.tax_var.get()
            tax = subtotal * (tax_percent / 100)
        except Exception:
            tax = 0.0

        self.lbl_tax.config(text=f"Tax: {tax:.2f}")
        total = subtotal + tax
        self.lbl_total.config(text=f"Total: {total:.2f}")

    def save_pdf(self):
        try:
            filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile=self.filename_var.get(),
            title="Save Invoice As"
            )

            if not filename:
                return  # user cancelled

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(0, 10, "Invoice", ln=True, align='C')
            pdf.ln(10)

            pdf.set_font("Arial", size=12)
            pdf.cell(95, 8, f"Seller: {self.seller_name_var.get()} ({self.seller_email_var.get()})", ln=0)
            pdf.cell(95, 8, f"Buyer: {self.buyer_name_var.get()} ({self.buyer_email_var.get()})", ln=1)
            pdf.cell(95, 8, f"Invoice No: {self.invoice_no_var.get()}", ln=0)
            pdf.cell(95, 8, f"Date: {self.date_var.get()}", ln=1)

            pdf.ln(10)

            pdf.set_font("Arial", "B", 12)
            pdf.cell(90, 10, "Description", border=1)
            pdf.cell(20, 10, "Qty", border=1, align='C')
            pdf.cell(30, 10, "Rate", border=1, align='C')
            pdf.cell(40, 10, "Amount", border=1, align='C')
            pdf.ln()

            pdf.set_font("Arial", size=12)
            for item in self.items:
                desc = item["desc"].get()
                qty = item["qty"].get()
                rate = item["rate"].get()
                amount = qty * rate

                pdf.cell(90, 10, desc, border=1)
                pdf.cell(20, 10, str(qty), border=1, align='C')
                pdf.cell(30, 10, f"{rate:.2f}", border=1, align='C')
                pdf.cell(40, 10, f"{amount:.2f}", border=1, align='C')
                pdf.ln()

            pdf.ln(5)
            pdf.cell(140, 10, "Subtotal:", align='R')
            pdf.cell(40, 10, f"{self.lbl_subtotal.cget('text').split(': ')[1]} {self.currency_var.get()}", align='R', ln=1)

            pdf.cell(140, 10, f"Tax ({self.tax_var.get()}%):", align='R')
            pdf.cell(40, 10, f"{self.lbl_tax.cget('text').split(': ')[1]} {self.currency_var.get()}", align='R', ln=1)

            pdf.cell(140, 10, "Total:", align='R')
            pdf.cell(40, 10, f"{self.lbl_total.cget('text').split(': ')[1]} {self.currency_var.get()}", align='R', ln=1)

            pdf.ln(10)
            pdf.multi_cell(0, 10, f"Notes:\n{self.notes_text.get('1.0', 'end').strip()}")
            pdf.output(filename)

            messagebox.showinfo("Success", f"Invoice saved as '{filename}'")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save PDF:\n{e}")

if __name__ == "__main__":
    app = InvoiceGenerator()
    app.mainloop()
