$(document).ready(function()
{
    //Make our movie table sortable and colour it nicely*
    $('#movie-table').dataTable(
    {
        "bPaginate": false,
        "bProcessing": true,
        "aaSorting": [[2,'desc']],    //sort by the IMDB rating by default
    });

});


//for all the options, read here:
//http://datatables.net/ref