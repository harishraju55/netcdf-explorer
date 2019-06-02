// This file is required by the index.html file and will
// be executed in the renderer process for that window.
// All of the Node.js APIs are available in this process.

const {ipcRenderer} = require('electron')

$("#dispfname").hide();
$('#fsub').hide();
$("#fileSpin").hide();
$("#fileCheck").hide();
$("#varSpin").hide();
$("#varCheck").hide();
$("#imgSec").hide();

$("#varSelection").hide();
$("#varCheck").height($("#varSelection").height());
$("#varSpin").height($("#varSelection").height());



$('#fsub').click(() => {
    var fpath = $('#fname')[0].files[0].path.replace(/\\/g, "/");
    var fname = $('#fname')[0].files[0].name;
    
    $("#fileSpin").show();
    // send file path to main process via IPC
    ipcRenderer.send('fpath-channel', fpath)
    
});

$('#fname').change(() => {
    var fname = $('#fname')[0].files[0].name;
    $("#dispfname").show();
    $("#fsub").show();
    $("#fileSpin").hide();
    $("#fileCheck").hide();
    $("#imgSec").hide();
    $("#dispfname").text(fname);
    $("#varSelection").hide();
    $("#varSpin").hide();
    $("#varCheck").hide();
    $('#fsub').prop("disabled", false);
});


$("select").change(() => {
    var varName = $('#varSelection :selected').text();
    $("#varCheck").hide();
    $("#varSpin").show();
    // sending file and variable info
    var fpath = $('#fname')[0].files[0].path.replace(/\\/g, "/");
    var fvar = { "fpath": fpath, "varName": varName}
    ipcRenderer.send('fpath-varName-channel', fvar);
});


// listen for variables list
ipcRenderer.on('variables-list-channel', (e, variableList) => {
    $("#varSelection").addClass("is-loading");
    $("#mySelect").empty()
    $('#mySelect').append($('<option>', { 
        value: '',
        text : 'select variable'
    }));
    $.each(variableList, function (i, item) {
        $('#mySelect').append($('<option>', { 
            value: item.name,
            text : item.value 
        }));
    });
    
    setTimeout(() => {
        $("#fileSpin").hide();
        $("#fileCheck").show();
        $('#fsub').prop("disabled", true);
        $("#varSelection").show();
        $("#varSelection").removeClass("is-loading");
        $("#varSelection").removeClass("is-warning");
        $("#varSelection").addClass("is-success");
    }, 3000)
    
})

// listen for var content
ipcRenderer.on('var-content-channel', (e, varContent) => {
    $("#varImg").attr('src', 'data:image/png;base64,'+varContent.plot);
    $("#varDesc").empty();
    var list = "";
    var descList = varContent.desc;
    for(i=0; i<descList.length; i++){
        list +="<li>"+descList[i].name+"</li>";
    }
    $("#varDesc").append(list);
    $("#varSpin").hide();
    $("#varCheck").show();
    $("#imgSec").show();
})
