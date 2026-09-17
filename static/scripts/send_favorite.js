$(document).ready(function() {
    // Specifically target .form-inline to avoid intercepting the "Back to Menu" form
    $('.form-inline').on('submit', function(event) {
        // Prevent standard page reload on form submit
        event.preventDefault();

        const form = $(this);
        const submitButton = form.find('.favorite-btn');

        // Optional: disable button briefly to prevent accidental duplicate clicks
        submitButton.prop('disabled', true);

        $.ajax({
            url: '/process_favorite',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                title: form.find('input[name="title"]').val(),
                image_url: form.find('input[name="image_url"]').val(),
                released: form.find('input[name="released"]').val(),
                rating: form.find('input[name="rating"]').val()
            })
        })
        .done(function(data) {
            console.log("AJAX success:", data);
            //alert(data.title + " added to favorites!");
            submitButton.text("Favorited!");
            submitButton.prop('disabled', true);
        })
        .fail(function(xhr, status, error) {
            console.error("AJAX error:", error);
            alert("Could not add to favorites. Check console for details.");
            submitButton.prop('disabled', false);
        });
    });
});