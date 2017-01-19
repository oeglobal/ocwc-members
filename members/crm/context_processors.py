from django.conf import settings

def invoice_years(request):
	return {
		'CURRENT_INVOICE_YEAR': settings.DEFAULT_INVOICE_YEAR, 
		'PREVIOUS_INVOICE_YEAR': settings.PREVIOUS_INVOICE_YEAR
	}