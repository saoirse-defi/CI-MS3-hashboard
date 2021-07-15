document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.sidenav');
    var instances = M.Sidenav.init(elems, {
        draggable: true
    });
  });

  
$(document).ready(function(){
    $('#ethTable').DataTable({
        "columns": [
            {"data": "date"},
            {"data": "hash"},
            {"data": "to"},
            {"data": "from"},
            {"data": "value"},
            {"data": "token"},
            {"data": "gasPrice"},
            {"data": "gasSpent"}
        ],
        "pagingType": "simple"
    });
    $('#erc20-table').DataTable({

    });
    $('.dataTables_length').addClass('bs-select');
    $('td').tooltip(); //bootstrap tooltip 
})

$(document).ready(() => {
    $('.modal').modal();
})


$('.carousel-slider').carousel({
    fullWidth: true
})