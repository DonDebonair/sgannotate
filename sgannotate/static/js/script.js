$(document).ready(function() {
    $('.annotation').editable({
        success: function(response, newValue) {
            var pk = $(this).data('pk');
            $('a[data-pk="' + pk + '"]').html(newValue).removeClass('editable-empty');
        }
    });
    $('[data-toggle="tooltip"]').tooltip();
});