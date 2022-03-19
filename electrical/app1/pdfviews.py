# from io import BytesIO
# from django.http import HttpResponse
# from django.template.loader import get_template

# from xhtml2pdf import pisa


# from django.views.generic import View
# from django.contrib.auth.models import User
# from datetime import datetime

# def render_to_pdf(template_src, context_dict={}):
#     template = get_template(template_src)
#     html  = template.render(context_dict)
#     result = BytesIO()
#     pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
#     if not pdf.err:
#         return HttpResponse(result.getvalue(), content_type='application/pdf')
#     return None


# class GeneratePDF(View):
#     def get(self, request, *args, **kwargs):
#         template = get_template('pdf.html')
#         customers = User.objects.all()
#         myDate = datetime.now()
#         formatedDate = myDate.strftime("%Y-%m-%d %H:%M:%S")
        
#         context={'customers':customers,'myDate':formatedDate}
       
#         html = template.render(context)
#         pdf = render_to_pdf('pdf.html', context)
#         if pdf:
#             response = HttpResponse(pdf, content_type='application/pdf')
#             filename = "Invoice_%s.pdf" %("12341232")
#             content = "inline; filename='%s'" %(filename)
#             download = request.GET.get("download")
#             if download:
#                 content = "attachment; filename='%s'" %(filename)
#             response['Content-Disposition'] = content
#             return response
        
#         return HttpResponse("Not found")
    
    
# import io
# from django.http import FileResponse
# from reportlab.pdfgen import canvas

# def some_view(request):
#     # Create a file-like buffer to receive PDF data.
#     buffer = io.BytesIO()

#     # Create the PDF object, using the buffer as its "file."
#     p = canvas.Canvas(buffer)

#     # Draw things on the PDF. Here's where the PDF generation happens.
#     # See the ReportLab documentation for the full list of functionality.
#     p.drawString(100, 100, "Hello world.")

#     # Close the PDF object cleanly, and we're done.
#     p.showPage()
#     p.save()

#     # FileResponse sets the Content-Disposition header so that browsers
#     # present the option to save the file.
#     buffer.seek(0)
#     return FileResponse(buffer, as_attachment=True, filename='hello.pdf')
