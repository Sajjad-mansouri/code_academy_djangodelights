$(document).ready(function(){
	
	var prefix = $('#forms_data').data('prefix');
	var ndx = $('#forms_data').data('extra');


	$('.add-row a').click(function(){
	var row = $('.form-row:first').clone()
	row.find("*").each(function() {
                updateElementIndex(this, prefix, ndx);
            });
	const totalForms = $("#id_" + prefix + "-TOTAL_FORMS").prop("autocomplete", "off");
	$(totalForms).val(parseInt(totalForms.val(), 10) + 1);
	ndx += 1
	row.insertBefore('.add-row')
})
	

	const updateElementIndex = function(el, prefix, ndx) {
            const id_regex = new RegExp("(" + prefix + "-(\\d+))");
		const replacement = prefix + "-" + ndx;
          
            if (el.id) {
                el.id = el.id.replace(id_regex, replacement);
            }
            if (el.name) {
                el.name = el.name.replace(id_regex, replacement);
            }
                                };




})