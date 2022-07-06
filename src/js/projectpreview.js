$(function () {//windows.onload
    $("#name").on('input', function () {
        $('h2').html($("#name").val());
    });

    $("#icon").change(function () {
        if ($('#icon').val() == '1') {
        } else if ($('#icon').val() == '2') {
            $("#icon-place").html("<i class='fab fa-github'></i>");
        } else if ($('#icon').val() == '3') {
            $("#icon-place").html("<svg class='open-in-new' xmlns='http://www.w3.org/2000/svg' height='24px' viewBox='0 0 24 24'width = '24px' fill = '#000000' ><path d='M0 0h24v24H0V0z' fill='none' /><path d='M19 19H5V5h7V3H5c-1.11 0-2 .9-2 2v14c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2v-7h-2v7zM14 3v2h3.59l-9.83 9.83 1.41 1.41L19 6.41V10h2V3h-7z' /></svg > ");
        }
    })

    $('#link').on('input', function () {
        $('a').attr("href", $('#link').val());
    });

    $("#description").on('input', function () {
        $('p').text($("#description").val());
    });

    $("#image").on('input', function () {
        $('img').attr("src", $('#image').val());
    });
});
