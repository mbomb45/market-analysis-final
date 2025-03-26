
from flask import Flask, render_template, request, send_file
from fpdf import FPDF
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.form.to_dict(flat=True)
    upgrades = request.form.getlist('upgrades')

    rent_increase = len(upgrades) * 60
    upgrade_cost = len(upgrades) * 1500
    roi = (rent_increase * 12) / upgrade_cost * 100 if upgrade_cost else 0
    payback = upgrade_cost / (rent_increase * 12) if rent_increase else 0

    content = f"""Property Name: {data.get('property_name')}
Location: {data.get('location')}
Construction Year: {data.get('construction_year')}
Occupancy Rate: {data.get('occupancy_rate')}%
Upgrades: {', '.join(upgrades)}
Estimated Rent Increase: ${rent_increase}
ROI: {roi:.2f}%
Payback Period: {payback:.2f} years"""

    pdf_path = generate_pdf_report(content)
    return render_template('results.html', data=data, upgrades=upgrades, rent_increase=rent_increase, roi=roi, payback=payback)

def generate_pdf_report(content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "Market Analysis Report", ln=True, align='C')
    pdf.ln(10)
    pdf.multi_cell(0, 10, content)
    pdf.output("report.pdf")
    return "report.pdf"

@app.route('/download_report')
def download_report():
    return send_file("report.pdf", as_attachment=True)

if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=10000)
