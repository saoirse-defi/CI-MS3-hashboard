document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.sidenav');
    var instances = M.Sidenav.init(elems, {
        draggable: true
    });
  });

$(document).ready(() => {
    $('.modal').modal();
})


$('.carousel-slider').carousel({
    fullWidth: true
})