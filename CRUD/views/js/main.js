$(document).ready(function(){
    eel.fetchalldata()
     
  $("#btn_addnew").on("click", function() {
    $("#Addnewmodal").show();
  });
  $(".close").on("click", function() {
    $("#Addnewmodal").hide();
  });
   
  $(".closeedit").on("click", function() {
    $("#Edit_modal").hide();
  });  
  $(".closedelete").on("click", function() {
    $("#Delete_modal").hide();
  });
})
   
function link(target) {
    window.location.href=target;
}
 
eel.expose(action_out)
function action_out(registers){ 
    //alert("Show Table");
    registers.forEach(showdata)
}
 
eel.expose(action_edit)
function action_edit(editemployees){ 
   //alert(editemployees);
   editemployees.forEach(get_array_values)
}
 
function get_array_values(item, index){
    //alert(item);
    //alert(index);
    if (index == 0) {
        document.getElementById("id").value = item;
    } else if (index == 1) {
        document.getElementById("edit_name").value = item;
    } else if (index == 2) {
        document.getElementById("edit_position").value = item;
    } else if (index == 3) {
        document.getElementById("edit_office").value = item;
    }
    else {}
 
}
// SAVE 
async function save_edit(){
    $( "#myformedit" ).validate({
        messages: {
            edit_name: {
                required: "Please provide Name"
            },
            edit_position: {
                required: "Please provide Position"
            },
            edit_office: {
                required: "Please provide Office"
            },
        },
        submitHandler: function(form) {
            eel.btn_update($('#edit_name').val(),$('#edit_position').val(),$('#edit_office').val(),$('#id').val())
            //alert("Success");
        }
    });
}
         
function showdata(item, index){
    var get_table = document.getElementById("employeedatatable");
    var tr = document.createElement("tr");
    var td = document.createElement("td");
    var td2 = document.createElement("td");
    var td3 = document.createElement("td");
    var td4 = document.createElement("td");
    var td5 = document.createElement("td");
     
    var id = item[0]
    td.innerText = item[0]
    td2.innerText = item[1]
    td3.innerText = item[2]
    td4.innerText = item[3]
         
    td5.innerHTML = '<button type="button" class="btn" onclick="btn_edit('+ id +')">Edit</button> | <button type="button" class="btndelete" onclick="buttondelete(('+ id +'))">Delete</button>'
         
    get_table.appendChild(tr)
    tr.appendChild(td)
    tr.appendChild(td2)
    tr.appendChild(td3)
    tr.appendChild(td4)
    tr.appendChild(td5)
}
     
// NEW Employee
async function save_register_js(){
    $( "#myform" ).validate({
            messages: {
                txtfullname: {
                    required: "Please provide Name"
                },
                txtposition: {
                    required: "Please provide Position"
                },
                txtoffice: {
                    required: "Please provide Office"
                },
            },
            submitHandler: function(form) {
                eel.btn_save($('#txtfullname').val(),$('#txtposition').val(),$('#txtoffice').val())
            }
    });
};
     
eel.expose(save_return); 
function save_return(status){
    if (status == "success"){
        $('#return_register').text('New Employee completed successfully!');
        $('#txtfullname').val('');
        $('#txtposition').val('');
        $('#txtoffice').val('');
    }
    if (status == "failure"){
        $('#return_register').text('Error when registering, make sure you have no blank fields.');
    }
};
     
eel.expose(edit_return); 
function edit_return(status){
    if (status == "success"){
        $('#return_register').text('Employee Updated successfully!');
    }
    if (status == "failure"){
        $('#return_register').text('Error when updating, make sure you have no blank fields.');
    }
};
   
function buttondelete(id)
{
    document.getElementById("idvalue").value = id;
    $("#Delete_modal").show();
}
 
async function btn_edit(id){ 
    eel.get_employee(id)
    $("#Edit_modal").show();
}
 
async function btn_submitdelete(id){ 
    //alert(id);
    eel.get_delete_employee(id)
}
 
eel.expose(update_return); 
function update_return(status){
    if (status == "success"){
        $('#return_update').text('Employee Updated successfully!');
        $('#txtfullname').val('');
        $('#txtposition').val('');
        $('#txtoffice').val('');
    }
    if (status == "failure"){
        $('#return_update').text('Error when updating record, make sure you have no blank fields.');
    }
};
 
eel.expose(delete_return)
function delete_return(delemployees){ 
   alert(delemployees);
    if (status == "success"){
        location.href = "index.html";
    }
    if (status == "failure"){
        $('#return_delete').text('Error deleting record');
    }
}