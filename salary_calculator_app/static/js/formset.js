function show_new_form_HTML(father_id, formhtml, totalforms_id, maxforms_id, addbeforeobj_id)
{
	var fatherObj = document.getElementById(father_id);
	var newdiv = document.createElement("div");
	var totalformsObj = document.getElementById(totalforms_id);
    var maxformsObj = document.getElementById(maxforms_id);
    var addbeforeObj = document.getElementById(addbeforeobj_id);

	var totalforms = parseInt(totalformsObj.value);
    var maxforms = parseInt(maxformsObj.value);

    if (totalforms < maxforms) {
	    formhtml = formhtml.replace(/__prefix__/g, totalformsObj.value);
	    newdiv.innerHTML = formhtml;
	    $(newdiv).hide();
	    totalformsObj.value = totalforms + 1 + ""; // Asi lo convierto a String.
	    fatherObj.insertBefore(newdiv, addbeforeObj);
	    $(newdiv).slideDown("slow");
    }
}

function hide_father(node, totalforms_id) {
	//var delcheckObj = node.parentElement.parentElement.lastElementChild.children[0];
    var totalformsObj = document.getElementById(totalforms_id);
    var totalforms = parseInt(totalformsObj.value);
    totalformsObj.value = totalforms - 1 + "";
	$(node.parentElement.parentElement).slideUp("slow");
	//delcheckObj.checked = true; // Necesario para el django FORMSET.
}
