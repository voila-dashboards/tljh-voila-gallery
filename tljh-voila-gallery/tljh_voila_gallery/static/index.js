$(document).ready(function() {
    $('.launch-item').click(function(event) {
        var example = $(event.currentTarget).data('example-name');
        $('#example-' + example).prop('checked', true);
        $('#spawn_form').submit();
        return false;
    });
});
