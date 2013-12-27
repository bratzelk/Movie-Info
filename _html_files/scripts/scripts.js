$(document).ready( function () {
    $('#movie-table').dataTable( {
    
    "bPaginate": false,

    "bProcessing": true,

    //sort by the IMDB rating by default
    "aaSorting": [[2,'desc']],
    } );
} );


//for all the options, read here:
//http://datatables.net/ref