from django.shortcuts import render
from rest_framework import viewsets, status
from .models import Invoice, Waybill, Receipt
from .serializers import InvoiceSerializer, WaybillSerializer, ReceiptSerializer
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from django.conf import settings

# generate invoice as pdf
def generate_invoice_as_pdf(request):
    #get the invoice instance
    invoice = Invoice()

    # create a buffer to reciewve PDF data
    buffer = BytesIO()

    # create a new PDF object using the buffer as its file
    p = canvas.Canvas(buffer, pagesize=letter)

    # set font size
    p.setFont("Helvetica", 12)

    # draw things on the PDF. Here's where the PDF generation happens.
    p.drawString(100, 750, "Invoice")
    p.drawString(100, 720, f"Due Date: {invoice.payment_due_date}")
    p.drawString(100, 700, f"Notes: {invoice.notes}")
    p.drawString(100, 680, f"Signature: {invoice.signature}")
    p.drawString(100, 660, f"Sent: {invoice.sent}")
    p.drawString(100, 640, f"Invoice Date: {invoice.invoice_date}")
    p.drawString(100, 620, f"Sent By: {invoice.sent_by}")
    p.drawString(100, 600, f"Delivered To: {invoice.delivered_to}")
    p.drawString(100, 580, f"Service: {invoice.service}")
    p.drawString(100, 560, f"Service Details: {invoice.service_details}")
    p.drawString(100, 540, f"Quantity: {invoice.quantity}")
    p.drawString(100, 520, f"Weight: {invoice.weight}")
    p.drawString(100, 500, f"Unit Price: {invoice.unit_price}")
    p.drawString(100, 480, f"Total Price: {invoice.total_price}")

    # save PDF to buffer
    p.showPage()
    p.save()

    # Read buffer
    buffer.seek(0)
    return buffer


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    # send invoice via email
    @action(detail=True, methods=['post'])
    def send_invoice(self, request, pk=None):
        invoice = self.get_object()

        # generaate the invoice as pdf
        pdf_invoice = generate_invoice_as_pdf(invoice)

        # create an email message
        msg = MIMEMultipart()
        msg['From'] = "cubeseed@gmail.com"
        msg['To'] = invoice.delivered_to.user.email
        msg['Subject'] = "Invoice for your order"

        # Attach the pdf invoice
        pdf_attachment = MIMEApplication(pdf_invoice.read(), _subtype="pdf")
        # Close the pdf_invoice
        pdf_invoice.close()
        pdf_attachment.add_header('Content-Disposition', 'attachment', filename='invoice.pdf')
        msg.attach(pdf_attachment)

        # send the emial using SMTP
        smpt_server = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_username = settings.EMAIL_HOST_USER
        smtp_password = settings.EMAIL_HOST_PASSWORD
        smpt_server.starttls()
        smpt_server.login(smtp_username, smtp_password)
        smpt_server.sendmail(msg['From'], msg['To'], msg.as_string())
        smpt_server.quit()

        # update the invoice sent status to sent
        invoice.sent = True
        invoice.save()
        return Response({'status': 'invoice sent successfully'}, status=status.HTTP_200_OK)


class WaybillViewSet(viewsets.ModelViewSet):
    queryset = Waybill.objects.all()
    serializer_class = WaybillSerializer

    @action(detail=True, methods=['post'])
    def send_waybill(self, request, pk=None):
        waybill = self.get_object()
        # implement the loginc to send an waybill
        waybill.sent = True
        waybill.save()
        return Response({'status': 'waybill sent successfully'})


class ReceiptViewSet(viewsets.ModelViewSet):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer

    @action(detail=True, methods=['post'])
    def send_receipt(self, request, pk=None):
        receipt = self.get_object()
        # implement the loginc to send an receipt
        receipt.sent = True
        receipt.save()
        return Response({'status': 'receipt sent successfully'})
