from flask import Flask, request, send_file
import os
from fpdf import FPDF
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

@app.route('/gumroad-ping', methods=['POST'])
def gumroad_ping():
    data = request.form
    email = data.get('email')
    product_id = data.get('product_id')

    if product_id == 'YOUR_GUMROAD_PRODUCT_ID':
        ebook_path = generate_ebook(email)
        send_email(email, ebook_path)

    return '', 200

def generate_ebook(email):
    content = f"Hi {email}, this is your AI-generated eBook!"
    filename = f"{email}_ebook.pdf"
    filepath = os.path.join('ebooks', filename)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, content)
    pdf.output(filepath)

    return filepath

def send_email(to_email, ebook_path):
    msg = EmailMessage()
    msg['Subject'] = 'Your AI eBook is Ready'
    msg['From'] = 'your_email@gmail.com'
    msg['To'] = to_email
    msg.set_content('Thanks for your purchase! Your eBook is attached.')

    with open(ebook_path, 'rb') as f:
        msg.add_attachment(f.read(), maintype='application', subtype='pdf', filename=os.path.basename(ebook_path))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('your_email@gmail.com', 'your_app_password')
        smtp.send_message(msg)

if __name__ == "__main__":
    os.makedirs('ebooks', exist_ok=True)
    app.run(debug=True)
