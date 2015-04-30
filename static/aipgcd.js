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
function refillSelect(select, values){
    var select_class = $(select);
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

//Convert table to array
function tableToArray(id){
    var array = [];
    var headers = [];
    $('#'+id+' th').each(function(index, item) {
        headers[index] = $(item).text();
    });
    $('#'+id+' tr').has('td').each(function() {
        //var arrayItem = {};
        var arrayItem = [];
        $('td', $(this)).each(function(index, item) {
            arrayItem.push($(item).text());
        });
        array.push(arrayItem);
    });
    return [headers, array];
}

function samp_table(id, use_samp){
    var dataarr = tableToArray(id);
    coltypes = $('#'+id).attr('columns');
    $.ajax({type: 'POST',
            url: 'get_samp_table',
            data: {'samp': use_samp,
                    'coltypes': coltypes,
                    'header[]': dataarr[0],
                     'data[]': JSON.stringify(dataarr[1])},
            traditional: true,
            success: function(response, status, xhr){
                 if (use_samp) {
                     var connector = new samp.Connector("Sender");
                     var send = function(connection){
                         var msg = new samp.Message("table.load.votable", {"url": response});
                         connection.notifyAll([msg]);
                     }
                     connector.runWithConnection(send);
                 }
                 else{
                    var afilename = response.split('/');
                    var filename = afilename[afilename.length - 1];
                    var blob = new Blob([response], { type: "application/x-download" });
                    //var URL = window.URL || window.webkitURL;
                    var downloadUrl = response; //URL.createObjectURL(blob);
                    var a = document.createElement("a");
                    // safari doesn't support this yet
                    if (typeof a.download === 'undefined') {
                         window.location = downloadUrl;
                    } else {
                         a.href = downloadUrl;
                         a.download = filename;
                         document.body.appendChild(a);
                         a.click();
                    }
                    //window.location = downloadUrl;
                 }
             }});

}
