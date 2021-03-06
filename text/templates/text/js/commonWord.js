$(document).ready(function() {

$("#ignoreDefault").on("change", function() {
    var currentIgnoreText = $("#ignoreInput").val();
    var isDefaultKeywordPresent = currentIgnoreText.includes(API_IGNORE_DEFAULT_KEYWORD);

    if ($(this).is(':checked')) {
        if (!isDefaultKeywordPresent) {
            var prefixChar =
                (currentIgnoreText && currentIgnoreText[currentIgnoreText.length - 1] != "\n")
                ? "\n"
                : "";
            $("#ignoreInput").val($("#ignoreInput").val() + prefixChar + API_IGNORE_DEFAULT_KEYWORD + "\n");
        }
    }
    else {
        if (isDefaultKeywordPresent) {
            // currentIgnoreText = currentIgnoreText.replace(/ *\t* *__DEFAULT__ *\t* *\n?/g, '');
            currentIgnoreText = currentIgnoreText.replace(
                                    new RegExp("[\t ]*" + API_IGNORE_DEFAULT_KEYWORD + "[\t ]*\n?", "g"), '');
            $("#ignoreInput").val(currentIgnoreText);
        }
    }
});
$('#ignoreDefault').trigger('change');

$('#ignoreInput').on('keyup', function() {
    var currentIgnoreText = $(this).val();
    var isDefaultKeywordPresent = currentIgnoreText.includes(API_IGNORE_DEFAULT_KEYWORD);

    if (isDefaultKeywordPresent) {
        $("#ignoreDefault").prop("checked", true); // $('#ignoreDefault').attr("checked", true);
    }
    else {
        $("#ignoreDefault").prop("checked", false); // $('#ignoreDefault').removeAttr("checked");
    }
});

});

var API_IGNORE_DEFAULT_KEYWORD = "__DEFAULT__";
