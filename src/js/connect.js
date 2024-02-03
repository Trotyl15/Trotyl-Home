$(function () {
    $('.discord').click(function () {
        $('.discord>.toast').addClass("active")
        var copyText = ".trotyl.";
        copyToClipboard(copyText);
        setTimeout(function() { $('.discord>.toast').removeClass("active"); }, 400);
    })
    $('.switch').click(function () {
        $('.switch>.toast').addClass("active")
        var copyText = "SW-0306-6465-4321";
        copyToClipboard(copyText);
        setTimeout(function() { $('.switch>.toast').removeClass("active"); }, 400);
    })
})

function copyToClipboard(text) {
    var sampleTextarea = document.createElement("textarea");
    document.body.appendChild(sampleTextarea);
    sampleTextarea.value = text; //save main text in it
    sampleTextarea.select(); //select textarea contenrs
    document.execCommand("copy");
    document.body.removeChild(sampleTextarea);
}