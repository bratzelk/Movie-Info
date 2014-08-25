$(document).ready(function()
{
    //Make our movie table sortable and colour it nicely*
    $('#movie-table').dataTable(
    {
        "bPaginate": false,
        "bProcessing": true,
        "aaSorting": [[2,'desc']],    //sort by the IMDB rating by default
    });


    //hide the coverflow by default
    $("#coverflow").hide();
    $("#coverflow-meta").hide();

    //show hide the coverflow when they click the link
    $("#coverflow-toggle").click(function (e) {
        $("#coverflow").toggle();
        $("#coverflow-meta").toggle();
        //trigger the resize event so it redraws the coverflow
        $(window).trigger('resize');
        e.preventDefault();
    });

    //Do the actual coverflow
    $('#coverflow').coverflow({
        index:          0,
        density:        1.2,
        innerOffset:    20,
        innerScale:     .65,
        innerAngle:     -55,
        outerAngle:     -40,

        //add the selected title when they select a new one from the coverflow
        select:         function(event, cover){
                            var img = $(cover).children().andSelf().filter('img').last();
                            $('#coverflow-meta').text(img.data('title') || 'unknown');
                        }
    
    });

    $("[data-toggle='tooltip']").tooltip(); 

});


//for all the options, read here:
//http://datatables.net/ref