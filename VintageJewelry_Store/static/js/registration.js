var url = $("#Url").attr("data-url");

$("#registration").submit(function (e) {
    // preventing default actions
    e.preventDefault();
    // serialize the data for sending the form data.
    var serializedData = $(this).serialize();
    // Ajax Call
    $.ajax({
        type: 'POST',
        url: url,
        data: serializedData,
        // handle a successful response
        success: function (response) {
            // On successful, clear all form data
            $("registration").trigger('reset');
            console.log(response)
        },
        error: function (response) {
            // alert non successful response
            console.log(response)
            alert(response["responseJSON"]["error"]);

            //$("registration").replaceWith(response['responseJSON']['error']);
        }
    })
})