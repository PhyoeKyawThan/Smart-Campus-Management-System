from flask import Flask, Response
from xhtml2pdf import pisa
import io

def generate_pdf():
    # HTML content
    html_content = '''
    <html>
    <head>
        <style>
            h1 { color: blue; }
            p { font-size: 16px; }
        </style>
    </head>
    <body>
        <h1>Hello, World!</h1>
        <p>This is a sample PDF generated from HTML.</p>
    </body>
    </html>
    '''
    
    # Convert HTML to PDF
    buffer = io.BytesIO()
    pisa.CreatePDF(io.StringIO(html_content), dest=buffer)
    buffer.seek(0)

    # Return PDF as response
    return Response(buffer, mimetype='application/pdf', headers={"Content-Disposition": "attachment;filename=example.pdf"})

