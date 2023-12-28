import datetime
import io
import os
# Python things
import platform
import traceback
from pathlib import Path

# Third party things
import pdfkit
# or
from django.conf import \
    settings  # Here you can import almost every thing in settings.py
from django.core.mail import EmailMessage, get_connection, send_mail
# Django things
from django.shortcuts import render
from django.template.loader import get_template, render_to_string

meses = {
    1: 'Enero',
    2: 'Febrero',
    3: 'Marzo',
    4: 'Abril',
    5: 'Mayo',
    6: 'Junio',
    7: 'Julio',
    8: 'Agosto',
    9: 'Septiembre',
    10: 'Octubre',
    11: 'Noviembre',
    12: 'Diciembre',
}

"""
- Usage:
from .emailer import sendRegisterMail
context = [
    'email': form.cleaned_data['email'], 
    'email_content': {
        "username": username,
        "url": activate_url,
    }, 
    'subject': "Registro",
    'body_template': "email/registro_responsiva.html",
    'attachment': True,
    'file_properties': {
        'file_path': 'static/assets/documents/Responsiva.pdf',
        'file_name': 'Responsiva.pdf'
    }
]
"""
def create_mail_connection_as_interno(context):
    with get_connection(
        host=os.getenv('EMAIL_HOST'), 
        port=os.getenv('EMAIL_PORT'), 
        username=os.getenv('EMAIL_HOST_USER_INTERNO'), 
        password=os.getenv('EMAIL_HOST_PASSWORD_INTERNO'), 
        use_tls=os.getenv('EMAIL_USE_TLS') == 'True',
    ) as connection:
        mail = EmailMessage(
            context['subject'],
            render_to_string(context['body_template'], context['email_content']),
            os.getenv('EMAIL_HOST_USER_INTERNO'),
            [context['email']],
            connection=connection
        )
    return mail



def sendMail(context):
    try:
        # log({
        #     'action': 'send_mail_responsiva' if context.get('attachment', None) else 'send_mail_credentials',
        #     'email': context.get('email', None),
        #     'subject': context.get('subject', None),
        # })
        # Config email
        mail = create_mail_connection_as_interno(context)
        mail.content_subtype = "html"

        if context['attachment']:
            pdf = generate_pdf(context)
            pdf_file = io.BytesIO(pdf)
            pdf_file.name = "Acuse.pdf"
            mail.attach(pdf_file.name, pdf_file.read(), "application/pdf")
        mail.send()
        #print("Email sent")
    except Exception:
        traceback.print_exc()
        # log({
        #     'action': 'send_mail',
        #     'error_message': traceback.format_exc(),
        # })




def generate_pdf(data):
    # Get the data
    # Get the template
    template = get_template(data.get('template'))
    # Render the data in the template
    html = template.render(data)
    
    # options to config pdfkit
    options = {
        "page-size": 'Letter', # Page size 
        'title': "PDF title", # File title
        #'margin-top': '200px', # Margin top
        #'margin-right': '0px', # Margin right
        #'margin-left': '0px', # Margin left
        #'margin-bottom': '10px', # Margin botton
        'encoding': "ISO-8859-3", # File enconding, it can be UTF-8 but sometimes it does not work
        #'footer-html': 'templates/footer.html', # Footer
        #'--header-html': 'templates/header.html', # Header
        #'--header-spacing': '-223', # Header spacing from the content
        #'--footer-spacing': '-14', # Footer spacing from the content
        '--enable-local-file-access': "", # The pdf can access file from the local machine
    }
    
    # Config of wkhtmltopdf
    # Default is linux config else windows config
    config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf') \
        if platform.system() != 'Windows' \
        else pdfkit.configuration(
            # Windows config
            wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
    )
    # This is the path to the css
    # STATICFILES_DIRS[0] are the dirs to access the static files like js, css and images, css mus be load here or using cdn in html
    css = [
        f'{settings.STATICFILES_DIRS[0]}/assets/pdfbootstrap/css/bootstrap.min.css'
        # f'{settings.STATICFILES_DIRS[0]}/assets/css/styles.min.css', 
        # f'{settings.STATICFILES_DIRS[0]}/assets/pdfbootstrap/css/bootstrap.min.css',
        # etc
    ]
    
    # Generate the pdf from string using the rendered html, the options and the config, we can add the css, and write the path to save it, 
    # in this case is not saved, it is just rendered miau
    # to add css just write css=css and the save path is output_path='miau.pdf'
    pdf_file = pdfkit.from_string(html, options=options, configuration=config, css=css)
    
    return pdf_file
