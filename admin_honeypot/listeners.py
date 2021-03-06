from admin_honeypot.signals import honeypot
from django.conf import settings
from django.core.mail import mail_admins
from django.template.loader import render_to_string
from django.urls import reverse

# this is a receiver function, the honeypot signal sends two variables: instance, request
def notify_admins(instance, request, **kwargs):
    '''
    gathers details in context, render email through the template and send through django mail helper
    '''
    path = reverse('admin:admin_honeypot_loginattempt_change', args=(instance.pk,))
    admin_detail_url = 'http://{0}{1}'.format(request.get_host(), path)
    context = {
        'request': request,
        'instance': instance,
        'admin_detail_url': admin_detail_url,
    }
    subject = render_to_string('admin_honeypot/email_subject.txt', context).strip()
    message = render_to_string('admin_honeypot/email_message.txt', context).strip()
    # Django method to email site admins as defined in settings.py
    mail_admins(subject=subject, message=message)

# check attribute of settings, if True, register signal to receiver callback function (notify_admins)
if getattr(settings, 'ADMIN_HONEYPOT_EMAIL_ADMINS', True):
    honeypot.connect(notify_admins)
