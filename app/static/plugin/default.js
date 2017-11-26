$(document).ready(function()
{
/*$("select.country").change(function(){
var selectedCountry = $(".country option:selected").val();	
     alert("You have selected the country - " + selectedCountry);
});*/
var code=$(".codemirror-textarea")[0];
var editor=CodeMirror.fromTextArea(code,{
	lineNumbers:true
});

});
