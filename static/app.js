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

setTimeout(function() {
    $(".alert-success").fadeOut().empty();
  }, 3000);

  setTimeout(function() {
    $(".alert-danger").fadeOut().empty();
  }, 3000);
