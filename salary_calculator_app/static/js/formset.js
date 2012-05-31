function formset_init(formsetPrefix)
{
    var totalformsObj = document.getElementById("id_" + formsetPrefix + "-TOTAL_FORMS");
    totalformsObj.value = "1";
}

function show_new_form_HTML(father_id, divAttrs, divContent, formsetPrefix, addbeforeobj_id)
{
	var fatherObj = document.getElementById(father_id);
	var newdiv = document.createElement("div");
    var addbeforeObj = document.getElementById(addbeforeobj_id);

    if (get_total_forms(formsetPrefix) < get_max_forms(formsetPrefix))
    {
	    divContent = divContent.replace(/__prefix__/g, get_total_forms(formsetPrefix) + "");
	    newdiv.innerHTML = divContent;
        for (var attr in divAttrs)
            newdiv.setAttribute(attr, divAttrs[attr]);
	    $(newdiv).hide();

        increase_total_forms(formsetPrefix, 1);

	    fatherObj.insertBefore(newdiv, addbeforeObj);
	    $(newdiv).slideDown("slow");
    }
}

function hide_father(node, formsetPrefix)
{
    //decrease_total_forms(formsetPrefix, 1);
    var grandfather = node.parentElement.parentElement;
	$(grandfather).slideUp("slow");
    //grandfather.parentElement.removeChild(grandfather);
    var delcheckObj = node.parentElement.parentElement.lastElementChild.children[0];
	delcheckObj.checked = true; // Necesario para el django FORMSET.
}

function get_total_forms(formsetPrefix)
{
    var totalformsObj = document.getElementById("id_" + formsetPrefix + "-TOTAL_FORMS");
    var result = parseInt(totalformsObj.value);
    return result;
}

function get_max_forms(formsetPrefix)
{
    var maxformsObj = document.getElementById("id_" + formsetPrefix + "-MAX_NUM_FORMS");
    var result = parseInt(maxformsObj.value);
    return result;
}

function increase_total_forms(formsetPrefix, value)
{
    var totalformsObj = document.getElementById("id_" + formsetPrefix + "-TOTAL_FORMS");
    totalformsObj.value = get_total_forms(formsetPrefix) + value + ""; // Asi lo convierto a String.
}

function decrease_total_forms(formsetPrefix, value)
{
    var totalformsObj = document.getElementById("id_" + formsetPrefix + "-TOTAL_FORMS");
    totalformsObj.value = get_total_forms(formsetPrefix) - value + ""; // Asi lo convierto a String.
}
