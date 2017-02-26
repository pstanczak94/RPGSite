$(document).ready(function(){
    if ($('#next-page-seconds').length) {
        setTimeout(NextPageSwitch, 1000);
    }
});

function NextPageSwitch() {
    var seconds = $('#next-page-seconds').text() - 1;

    if (seconds > 0) {
        $('#next-page-seconds').text(seconds);
    } else {
        window.location = $('#next-page-url').text();
    }

    setTimeout(NextPageSwitch, 1000);
}