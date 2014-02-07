$(document).ready(function()
{
    //Make our movie table sortable and colour it nicely*
    $('#movie-table').dataTable(
    {
        "bPaginate": false,
        "bProcessing": true,
        "aaSorting": [[2,'desc']],    //sort by the IMDB rating by default
    });

    $('#coverflow').coverscroll({
        'titleclass':'coverflow-meta',
        'selectedclass':'coverflow-selected', 
        'scrollactive':false,
        'distribution':1.8,
        'scalethreshold':1,
        'step':{ // compressed items on the side are steps
            'limit': 6, // how many steps should be shown on each side
            'width': 0, // how wide is the visible section of the step in pixels
            'scale':false // scale down steps
        }
    });

});


//for all the options, read here:
//http://datatables.net/ref