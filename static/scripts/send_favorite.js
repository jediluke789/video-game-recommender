$(document).ready(function() {
    // Specifically target .form-inline to avoid intercepting the "Back to Menu" form
    $('.form-inline').on('submit', function(event) {
        // Prevent standard page reload on form submit
        event.preventDefault();

        const form = $(this);
        const submitButton = form.find('.favorite-btn');

        // Disable button to prevent accidental duplicate clicks
        submitButton.prop('disabled', true);
        // Call the AJAX function to send the favorite game data to the server
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
        // Handle the AJAX response and change the button text to "Favorited!" if successful, or re-enable the button if there was an error
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