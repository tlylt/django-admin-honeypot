from django.dispatch import Signal

# honeypot is a signal instance. There are two variables
honeypot = Signal(providing_args=['instance', 'request'])
