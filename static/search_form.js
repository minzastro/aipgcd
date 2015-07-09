/*
 * Functions to support dynamic search window.
 */
function fillSelect(select_class, values, names){
    //Fill select item with values and names
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
    // Remove current div.
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
    // Show or hide extra key condition fields
    var parent = elt.parentNode;
    var vis = "hidden";
    if (elt.selectedIndex == 2){
        // "extra" was selected:
        vis = "visible";
    }
    parent.childNodes[parent.childNodes.length - 2].style.visibility = vis;
    parent.childNodes[parent.childNodes.length - 3].style.visibility = vis;
}

function getTableDiv(condition_list, list){
  // Create a new table constraint
  var di = document.createElement('div');
  var label = document.createElement('label');
  label.setAttribute('for', 'table');
  di.appendChild(label);
  // Table constraint:
  var select = document.createElement('select');
  select.setAttribute('name', 'has_record');
  fillSelect(select, ['exists', 'not exists'], ['included', 'not included']);
  di.appendChild(select);
  // List of tables:
  var table_list = document.createElement('select');
  table_list.setAttribute('name', 'in_table');
  fillSelect(table_list, list, list);
  di.appendChild(table_list);
  createDeletionButton(di);
  document.getElementById(condition_list).appendChild(di);
}

function getKeyDiv(condition_list, key_list){
  // Create a new key constraint
  var di = document.createElement('div');
  var label = document.createElement('label');
  label.setAttribute('for', 'condition');
  di.appendChild(label);
  //Condition selector:
  var select = document.createElement('select');
  select.setAttribute('name', 'condition');
  select.setAttribute('onchange', 'showHideFields(this)');
  fillSelect(select, ['exists', 'not exists', 'extra'], ['has', 'has not', 'condition']);
  di.appendChild(select);
  //Key selector:
  var table_list = document.createElement('select');
  table_list.setAttribute('name', 'in_key');
  fillSelect(table_list, key_list, key_list);
  di.appendChild(table_list);
  //Unequality selector:
  var constraint = document.createElement('select');
  constraint.setAttribute('name', 'constraint');
  constraint.setAttribute('id', 'constraint');
  var constraint_list = ['=', '>', '<', '!=', '>=', '<=', 'like']
  fillSelect(constraint, constraint_list, constraint_list);
  di.appendChild(constraint);
  // Expression input:
  var expression = document.createElement('input');
  expression.setAttribute('name', 'expression');
  di.appendChild(expression);
  createDeletionButton(di);
  showHideFields(select);
  document.getElementById(condition_list).appendChild(di);
}

function getMOCDiv(moc_list, moc_names, moc_descr){
  var di = document.createElement('div');
  // MOC constraint:
  var select = document.createElement('select');
  select.setAttribute('name', 'has_moc');
  fillSelect(select, ['exists', 'not exists'], ['overlap', 'no overlap']);
  di.appendChild(select);
  // List of MOCs:
  var smoc_list = document.createElement('select');
  smoc_list.setAttribute('name', 'in_moc');
  fillSelect(smoc_list, moc_names, moc_descr);
  di.appendChild(smoc_list);
  createDeletionButton(di);
  document.getElementById(moc_list).appendChild(di);
}

function setFlagSelector(parent, value){
    if (value == 'xid_flag'){
        parent.getElementsByTagName('select')[2].style.visibility = 'visible';
        parent.getElementsByTagName('select')[3].style.visibility = 'hidden';
    } else {
        parent.getElementsByTagName('select')[3].style.visibility = 'visible';
        parent.getElementsByTagName('select')[2].style.visibility = 'hidden';
    }
}

function getFlagDiv(flag_list){
  var di = document.createElement('div');
  // MOC constraint:
  var select1 = document.createElement('select');
  select1.setAttribute('name', 'flag_name');
  fillSelect(select1, ['xid_flag', 'obs_flag'], ['xid_flag', 'obs_flag']);
  select1.addEventListener('change', function(){
      setFlagSelector(di, select1.options[select1.selectedIndex].innerText);
  });
  di.appendChild(select1);
  var select2 = document.createElement('select');
  select2.setAttribute('name', 'flag_constraint');
  fillSelect(select2, ['>=', '<='], ['>=', '<=']);
  di.appendChild(select2);
  var select3 = document.createElement('select');
  select3.setAttribute('name', 'xid_values');
  fillSelect(select3, ['-1', '0', '1', '2'],
                        ['-1: Not a cluster', '0: Undecided',
                         '1: Confirmed cluster', '2: Confirmed cluster with spectra']);
  di.appendChild(select3);
  var select4 = document.createElement('select');
  select4.setAttribute('name', 'obs_values');
  fillSelect(select4, ['0', '1', '2', '3'],
                        ['0: No data', '1: In a large survey',
                         '2: Dedicated photometry', '3: Dedicated spectroscopy']);
  di.appendChild(select4);
  setFlagSelector(di, select1.options[0].innerText);
    createDeletionButton(di);
  document.getElementById(flag_list).appendChild(di);
}
