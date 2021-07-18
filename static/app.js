document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.sidenav');
    var instances = M.Sidenav.init(elems, {
        draggable: false
    });
  });

$(document).ready(() => {
    $('.modal').modal();
    $('.sidenav').sidenav();
})


$('.carousel-slider').carousel({
    fullWidth: true
})