$(document).ready(function() {

// Enable popover elements
$(function() {
    $('[data-toggle="popover"]').popover();
});

// Support timeout on popover elements
$('[data-toggle="popover"][data-timeout]').on('shown.bs.popover', function() {
    this_popover = $(this);
    setTimeout(function() {
        this_popover.popover('hide');
    }, $(this).data("timeout"));
});

// Enable copying of target element contents
$('.mimr-btn-copy').on('click', function() {
    /* Get the text field */
    var toCopy = $(this).data("target");
    var copyText = document.getElementById(toCopy);

    /* Select the text field */
    copyText.select();
    copyText.setSelectionRange(0, 99999); /*For mobile devices*/

    /* Copy the text inside the text field */
    document.execCommand("copy");

    // Deselect the text
    copyText.blur();

    /* Alert the copied text */
    // alert("Copied the text: " + copyText.value); // I replaced this with popover
});

// Display selected filename when using Bootstrap custom-file-input
// This requires that the order of elements should be custom-file-input then custom-file-label
$('.custom-file-input').on('change', function() {
   let fileName = $(this).val().split('\\').pop();
   $(this).next('.custom-file-label').addClass("selected").html(fileName);
});

$('.serviceForm').on('submit', function(event) {
    event.preventDefault(); // prevent redirecting post request to server
    var formData = new FormData(this); // new FormData($("#serviceForm")[0])
    var urlValue = $(this).data("url"); // "/service/text/commonword/api/"
    var resultObj = $(this).data("result");

    var listElementsStr = $(this).data("list");
    if (listElementsStr) {
        var listElements = listElementsStr.split(' ');
        console.log("Transforming into list of strings the value of elements", listElements);
        for (var index = 0; index < listElements.length; ++index) {
            var targetAttribute = $(listElements[index]).attr("name");
            if (!targetAttribute) {
                console.log("Warning. Missing name for", listElements[index]);
                continue;
            }
            var arrayOfLines = $(listElements[index]).val().split('\n');
            var stringifiedList = JSON.stringify(arrayOfLines);
            formData.set(targetAttribute, stringifiedList);
        }
    }

    var spinnerObjects = $("span[class^='spinner-'],span[class*=' spinner-']");
    var spinners = $(this).find(spinnerObjects);

    var btnSubmit = $(this).find("button[type=submit]:focus");
    formData.set($(btnSubmit).attr("name"), $(btnSubmit).val());

    $.ajax({
        url: urlValue,
        type: "post",

        // headers: {'Authorization' : 'JWT sometoken'},
        data: formData,
        // data: $('.serviceForm').serialize(),
        // data: JSON.stringify( { "first-name": $('#first-name').val(), "last-name": $('#last-name').val() } ),

        crossDomain: true,
        processData: false,
        contentType: false, // 'application/json'
        // dataType: 'json',

        beforeSend: function(jqXHR, settings) {
            spinners.removeClass("d-none");
            console.log("Processing request...");
            $(resultObj).text("Currently processing...");
            $(resultObj).val("Currently processing..."); // for elements such as input type=text
        },
        success: function(data, textStatus, jqXHR){
            console.log("Request successful; textStatus:", textStatus);
            var dataStr = "";

            // TODO: Design a way to dynamically display different types of responses
            if (typeof(data) == "string") {
                dataStr = data;
            }
            else {
                // $.each(data, function(index, object) {
                //     $.each(object, function(word, count) {
                //         dataStr += word + " : " + count + "\n";
                //     });
                // });
                // or
                for (var index = 0; index < data.length; ++index) {
                    for (var key in data[index]) {
                        dataStr += key + " : " + data[index][key] + "\n";
                    }
                }
                // or
                // dataStr = JSON.stringify(data);
            }

            $(resultObj).text(dataStr);
            $(resultObj).val(dataStr);
        },
        error: function(jqXHR, textStatus, errorThrown){
            var msg = "Request error; textStatus: " + textStatus + " ; errorThrown: " + errorThrown;
            console.log(msg);
            $(resultObj).text(msg);
            $(resultObj).val(msg);
        },
    })
    // would only be called if there are no errors with the HTTP Request
    .done(function(data, textStatus, jqXHR) {
            console.log("Request done; textStatus:", textStatus); // alert("Request processing done");
        })
    // if something went wrong with the HTTP request, like if server has no response, resource does
    // not exist, rejected request, etc.
    .fail(function(jqXHR, textStatus, errorThrown) {
            // error types are timeout, error, abort, parseerror
            console.log("Request failed; textStatus:", textStatus, "; errorThrown:", errorThrown);
        })
    // would be called whether the HTTP Request was successful or not
    .always(function(data) { // data|jqXHR, textStatus, jqXHR|errorThrown
            console.log("Request ended");
            spinners.addClass("d-none");
        });
});

$('.mimr-strip-whitespace').on('change', function() {
    var strippedText = $(this).val();
    strippedText = strippedText.replace(/^[\t ]*/g, '');
    strippedText = strippedText.replace(/[\t ]*$/g, '');
    strippedText = strippedText.replace(/[\t ]*\n/g, '\n');
    strippedText = strippedText.replace(/\n[\t ]*/g, '\n');
    strippedText = strippedText.replace(/\n*\n/g, '\n');

    $(this).val(strippedText);
});

});
