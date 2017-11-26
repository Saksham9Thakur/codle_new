$(document).ready(function()
{
$("select.country").change(function(){
var selectedCountry = $(".country option:selected").val();	

});
var code=$(".codemirror-textarea")[0];
var editor=CodeMirror.fromTextArea(code,{
	lineNumbers:true,
	theme:"base16-dark"
});

});
