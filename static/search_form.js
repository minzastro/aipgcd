function fillSelect(select_class, values, names){
    //select_class.empty();
    if (values.length > 0){
        for (var i = 0; i < values.length; i++){
            var opt = document.createElement('option');
            opt.value = values[i];
            opt.textContent = names[i];
            select_class.appendChild(opt);
        }
    }
    else{
        var opt = document.createElement('option');
        opt.value = 'none';
        opt.textContent = '-';
        select_class.appendChild(opt);
    }
}

function deleteDiv(elt){
    var parent = elt.parentNode;
    parent.parentNode.removeChild(parent);
}

function createDeletionButton(div){
  var button = document.createElement('input');
  button.setAttribute('type', 'button');
  button.setAttribute('value', 'X');
  button.setAttribute('onclick', 'deleteDiv(this)');
  div.appendChild(button);
}

function showHideFields(elt){
    var parent = elt.parentNode;
    var vis = "hidden";
    if (elt.selectedIndex == 2){
        vis = "visible";
    }
    parent.childNodes[parent.childNodes.length - 2].style.visibility = vis;
    parent.childNodes[parent.childNodes.length - 3].style.visibility = vis;
}

function getTableDiv(condition_list, list){
  var di = document.createElement('div');
  var label = document.createElement('label');
  label.setAttribute('for', 'table');
  di.appendChild(label);
  var select = document.createElement('select');
  select.setAttribute('name', 'has_record');
  fillSelect(select, ['exists', 'not exists'], ['included', 'not included']);
  di.appendChild(select);
  var table_list = document.createElement('select');
  table_list.setAttribute('name', 'in_table');
  fillSelect(table_list, list, list);
  di.appendChild(table_list);
  createDeletionButton(di);
  document.getElementById(condition_list).appendChild(di);
}

function getKeyDiv(condition_list, key_list){
  var di = document.createElement('div');
  var label = document.createElement('label');
  label.setAttribute('for', 'condition');
  di.appendChild(label);
  var select = document.createElement('select');
  select.setAttribute('name', 'condition');
  select.setAttribute('onchange', 'showHideFields(this)');
  fillSelect(select, ['exists', 'not exists', 'extra'], ['has', 'has not', 'condition']);
  di.appendChild(select);
  var table_list = document.createElement('select');
  table_list.setAttribute('name', 'in_key');
  fillSelect(table_list, key_list, key_list);
  di.appendChild(table_list);
  var constraint = document.createElement('select');
  constraint.setAttribute('name', 'constraint');
  constraint.setAttribute('id', 'constraint');
  var constraint_list = ['=', '>', '<', '!=', '>=', '<=', 'like']
  fillSelect(constraint, constraint_list, constraint_list);
  di.appendChild(constraint);
  var expression = document.createElement('input');
  expression.setAttribute('name', 'expression');
  di.appendChild(expression);
  createDeletionButton(di);
  document.getElementById(condition_list).appendChild(di);
}
