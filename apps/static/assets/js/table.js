function tableSearch() {
    let input, filter, table, tr, td, txtValue;

    //Intialising Variables
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    table = document.getElementById("myTable");
    tr = table.getElementsByTagName("tr");
    column_length = document.getElementById('myTable').rows[0].cells.length;

    for (i = 1; i < tr.length; i++) { // except (heading)
        count_td = 0;
        for (j = 0; j < column_length - 1; j++) {
            td = tr[i].getElementsByTagName("td")[j];
            if (td) {
                if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
                    count_td++;
                }
            }
        }
        if (count_td > 0) {
            tr[i].style.display = "";
        } else {
            tr[i].style.display = "none";
        }
    }

}