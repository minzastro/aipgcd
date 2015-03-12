//Set value of select:
function setSelectByValue(id, value) {
    var sel = document.getElementById(id);
    for(var i = 0, j = sel.options.length; i < j; ++i) {
        if(sel.options[i].innerHTML === value) {
           sel.selectedIndex = i;
           break;
        }
    }
}


//Fill dropdown box with an array of values
function refillSelect(id, values){
    var select_class = $(id);
    select_class.empty();
    if (values.length > 0){
        for (var i = 0; i < values.length; i++){
            var opt = document.createElement('option');
            opt.value = values[i];
            opt.textContent = values[i];
            select_class.append(opt);
        }
    }
    else{
        var opt = document.createElement('option');
        opt.value = 'none';
        opt.textContent = '-';
        select_class.append(opt);
    }
}

//Fill selector #id with a list of current table columns
function fillSelectWithColumns(id, addNone, setValue, value){
    $.post("get_table_columns?table={{table}}", function(response){
        var values = response.split(',');
        if (addNone){
            values.unshift('none');
        }
        select_class = document.getElementById(id);
        select_class.onchange = null;
        refillSelect('#'+id, values);
        if (setValue){
            setSelectByValue(id, value);
        }
    })
}
