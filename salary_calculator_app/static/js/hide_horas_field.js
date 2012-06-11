function show_horas(cargoObj)
{
    //console.debug("START: show_horas : " + cargoObj);

    var id = cargoObj.getAttribute("id").split("-");
    var formsetprefix = id[0] + "-" + id[1];
    var horasInfoObj = document.getElementById(formsetprefix + "-horas");
    var cargoPorHoraObj = document.getElementById(formsetprefix + "-pago_por_horas_info");
    var selectedCargo = cargoObj.options[cargoObj.selectedIndex].getAttribute("value");

    var cantHorasRowObj = horasInfoObj.parentElement.parentElement;

    var cargo_por_hora = false;
    for (var i=0; i<cargoPorHoraObj.options.length; i++) {
        var optObj = cargoPorHoraObj.options[i];
        if (optObj.getAttribute("value") == selectedCargo && optObj.innerHTML == "True") {
            cargo_por_hora = true;
            break;
        }
    }

    horasInfoObj.value = "1.0";

    if (cargo_por_hora) {
        cantHorasRowObj.style.display = "table-row";
        //console.debug("Showing horas field");
    }
    else {
        cantHorasRowObj.style.display = "none";
        //console.debug("Hidding horas field");
        var errorRowObj = document.getElementById(formsetprefix + "-horas-errors");
        if (errorRowObj != null) {
            //console.debug("Showing horas-errors row");
            errorRowObj.style.display = "none";
        }
    }

    //console.debug("END: show_horas");
}

function initial_show_horas(formsetPrefix)
{
    //console.debug("START: initial_show_horas() : " + formsetPrefix);
    id = "id_" + formsetPrefix;
    id = id + "-" + (get_total_forms(preunivPrefix)-1) + "-cargo";
    show_horas(document.getElementById(id));
    //console.debug("END: initial_show_horas");
}
