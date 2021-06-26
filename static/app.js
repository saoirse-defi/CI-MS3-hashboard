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