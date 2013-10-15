jQuery(document).ready(function($) {
	$(document).foundation();
	$('form.uniForm').uniform();

	$('.icon-question-sign').hover(function(){
		var $help_container = $(this).closest('.row').find('.help_container');
		var value = $(this).siblings('input').attr('value');

		$help_container.html($('.help-text-'+value).html());
	}, function(){
		var $help_container = $(this).closest('.row').find('.help_container');
		$help_container.html('');
	})

	var display_moa = function() {
		var moa_type = $('input[name="simplified_membership_type"]:checked').val();
		
		if (moa_type) {
			$('.organization_consortia').hide();
			$('.corporate_support_levels').hide();

			if (moa_type === 'institutional') {
				$('.organization_consortia').show();
			} else if (moa_type === 'corporate') {
				$('.corporate_support_levels').show();
			}

			$('.moa-wrapper').html($('.moa-'+moa_type).html());
			$('#div_id_moa_terms').show();
		}
	}

	$('input[name="simplified_membership_type"]').on('change', display_moa);
	display_moa();

	$('.terms-text').html($('#siteterms').html());
	$('.coppa-text').html($('#coppatext').html());

});