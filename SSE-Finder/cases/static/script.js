var table;
$(document).ready(function() {
    var filterCounter = 0;
    $('.datatable').DataTable( {
        // fixedHeader: {
        //     header: true,
        //     footer: true
        // },
        "lengthMenu": [[10, 20, 50], [10, 20, 50]],
        "order": [],
        "search": {regex: true},
        // initComplete: function () {
        //     this.api().columns(phpFilterColumns).every( function () {});
        // }
    });

} );