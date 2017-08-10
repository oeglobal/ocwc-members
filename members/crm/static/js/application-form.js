jQuery(document).ready(function ($) {
    $(document).foundation();
    $('form.uniForm').uniform();

    $('.icon-question-sign').hover(function () {
        var $help_container = $(this).closest('.row').find('.help_container');
        var value = $(this).siblings('input').attr('value');

        $help_container.html($('.help-text-' + value).html());
    }, function () {
        var $help_container = $(this).closest('.row').find('.help_container');
        $help_container.html('');
    })


    $('.moa-text').html($('.moa').html());
    $('.terms-text').html($('#siteterms').html());
    $('.coppa-text').html($('#coppatext').html());

});
