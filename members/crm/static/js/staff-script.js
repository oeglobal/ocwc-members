jQuery(document).ready(function($) {
	var display_billing_form_options = function() {
		var option = $('#id_log_type').find('input[type="radio"]:checked').val();
		$('.billing-form .hide-initial').hide();

		if (option === 'create_invoice') {
			$('#div_id_amount').closest('.hide-initial').show();
		} else if (option === 'send_invoice') {
			$('#div_id_first_name').closest('.hide-initial').show();
		} else if (option === 'paid_invoice') {

		}
	}

	$('#id_log_type').click(display_billing_form_options);
	display_billing_form_options();
});