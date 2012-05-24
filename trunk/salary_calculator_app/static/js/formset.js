function show_new_form_HTML(father_id, divAttrs, divContent, formsetPrefix, addbeforeobj_id)
{
	var fatherObj = document.getElementById(father_id);
	var newdiv = document.createElement("div");
	var totalformsObj = document.getElementById("id_" + formsetPrefix + "-TOTAL_FORMS");
    var maxformsObj = document.getElementById("id_" + formsetPrefix + "-MAX_NUM_FORMS");
    var addbeforeObj = document.getElementById(addbeforeobj_id);

	var totalforms = parseInt(totalformsObj.value);
    var maxforms = parseInt(maxformsObj.value);

    if (totalforms < maxforms) {
	    divContent = divContent.replace(/__prefix__/g, totalformsObj.value);
	    newdiv.innerHTML = divContent;
        for (var attr in divAttrs)
            newdiv.setAttribute(attr, divAttrs[attr]);
	    $(newdiv).hide();
	    totalformsObj.value = totalforms + 1 + ""; // Asi lo convierto a String.
	    fatherObj.insertBefore(newdiv, addbeforeObj);
	    $(newdiv).slideDown("slow");
    }
}

function hide_father(node, formsetPrefix)
{
    var totalformsObj = document.getElementById("id_" + formsetPrefix + "-TOTAL_FORMS");
    var totalforms = parseInt(totalformsObj.value);
    totalformsObj.value = totalforms - 1 + "";
	$(node.parentElement.parentElement).slideUp("slow");
	//delcheckObj.checked = true; // Necesario para el django FORMSET.
}
