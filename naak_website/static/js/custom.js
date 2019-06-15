$(document).ready(function () {
    // $('#wrapwrap > header.o_affix_enabled > nav').css("display","none");
    $(".js-scroll-trigger").click(function() {
            debugger;
            event.preventDefault();
            $('html, body').animate({
            scrollTop: $("#section_spt").offset().top
        }, 2000);
    });
});