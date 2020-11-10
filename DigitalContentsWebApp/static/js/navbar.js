/*
This JavaScript function comes from https://bootstrapious.com/p/bootstrap-sidebar,
it provides the hamburger button with functionality
*/
$(document).ready(function () {

    $('#sidebarCollapse').on('click', function () {
        $('#sidebar').toggleClass('active');
    });

});