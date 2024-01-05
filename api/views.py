from django.views.decorators.csrf import csrf_protect,csrf_exempt,ensure_csrf_cookie
# from django.middleware.csrf import get_token
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.http import JsonResponse
import json
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


# def get_csrf_token(request):
#     return JsonResponse({'csrfToken': get_token(request)})
       
@csrf_exempt
def contactus(request):
    if request.method == "POST":
        data = json.loads(request.body)
        firstname = data.get('firstname', None)
        lastname = data.get('lastname', None)
        email = data.get('email', None)
        mobile = data.get('mobile', None)
        message = data.get('message', None)
        
        templateData = {
            'firstname': firstname,
            'lastname': lastname,
            'email': email,
            'mobile': mobile,
            'message': message,
        }
        
        try:
            email_content = render_to_string('emailtemplate.html', templateData)
            API = settings.APIKEY
            from_email = settings.FROM
            to_emails = settings.TO
            subject = 'Website Inquiry'
            html_content = email_content
            # template = email_content
            
            message = Mail(from_email,to_emails,subject)
            # message.content_type = "html"
            message.template_id = 'd-c0ac853076cf499785f1a24ab4f16a2f'
            message.dynamic_template_data = templateData
            try:
                sg = SendGridAPIClient(API)
                response = sg.send(message)
                print(response.status_code)
                print(response.body)
                print(response.headers)
            except Exception as e:
                print(e.message)
            
            
            # email = EmailMessage(
            #     'Website Inquiry',                  # Email subject
            #     email_content,                      # Email content from the template
            #     settings.DEFAULT_FROM_EMAIL,        # Sender's email
            #     [settings.DEFAULT_TO_EMAIL],        # Recipient's email
            # )
            # email.content_subtype = 'html'
            # email.send()
            print("Email Sent")
            return JsonResponse({ 'status': True })
        
        except Exception as e:
            print("Email sending failed")
            return JsonResponse({ 'status': False })

    