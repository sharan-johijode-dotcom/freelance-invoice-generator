# Invoice / PDF Generator (Offline)

Hey there! 👋
This is a simple offline Invoice Generator built with Python and Tkinter. It lets you create professional-looking invoices with multiple items and export them as PDF files and no internet required.

Perfect for freelancers, small businesses, or anyone who needs quick invoices without complicated software.

## Features

- Clean and user-friendly GUI
- Add unlimited invoice items (description, quantity, rate)
- Automatic subtotal, tax, and total calculation
- Custom tax percentage
- Multiple currency options (USD, EUR, GBP, INR)
- Seller & buyer details (name, email, invoice number, date)
- Notes section for custom messages
- Save invoices as PDF files
- Fully offline "no data leaves your computer"

## What You Need

Before you get started, make sure you have:
- Python 3.8+ installed
- Tkinter (comes with Python by default)
- fpdf library for PDF generation
> Install the required dependency:
```
 pip install fpdf
```
- Optional: PyInstaller if you want a standalone app

## How to Get It Running (Step by Step)

1. Clone the repository (or download it as ZIP):
```
git clone https://github.com/sharan-johijode-dotcom/freelance-invoice-generator.git
cd freelance-invoice-generator
```

2. Install the required library:
```
pip install fpdf
```

3. Run the app:
```
python invoice-app-freelancer.py
```

4. Use it:

- Enter seller and buyer details
- Add items (description, quantity, rate)
- Set tax percentage and currency
- Add notes if needed
- Click “Save PDF”
- Choose where to save your invoice

And that’s it! 🎉

## Make It a Standalone App (Optional)

Want to share this app without requiring Python? You can convert it into a single executable.

1. Install PyInstaller:
```
pip install pyinstaller
```

2. Build the executable :
```
#Windows
pyinstaller --onefile --windowed --icon=icon.ico invoice-app-freelancer.py

Mac
pyinstaller --onefile --windowed invoice-app-freelancer.py

Linux/unix
pyinstaller --onefile invoice-app-freelancer.py
```

3. Find your app in the dist/ folder:
```
dist/invoice-app-freelancer(.exe/.app/.deb)
```

Double-click it and it runs just like a normal app (Windows).


## Things to Keep in Mind

- This is a basic invoice generator (no database or history yet)
- Currency symbols are not shown, only currency codes
- Large descriptions may wrap differently in the PDF
- Fonts are kept simple for maximum compatibility
