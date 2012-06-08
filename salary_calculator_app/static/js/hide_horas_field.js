function showHoras(cargoObj)
{
    var id = cargoObj.getAttribute("id").split("-");
    var formsetprefix = id[0] + "-" + id[1];
    var horasInfoObj = document.getElementById(formsetprefix + "-horas");
    var cargoPorHoraObj = document.getElementById(formsetprefix + "-pago_por_horas_info");
    var selectedCargo = cargoObj.options[cargoObj.selectedIndex].getAttribute("value");

    var cantHorasRowObj = horasInfoObj.parentElement.parentElement;

    var cargo_por_hora = false;
    for (var i=0; i<cargoPorHoraObj.options.length; i++) {
        var optObj = cargoPorHoraObj.options[i];
        if (optObj.getAttribute("value") == selectedCargo && optObj.innerText == "True")
            cargo_por_hora = true;
            break;
    }

    if (cargo_por_hora)
        cantHorasRowObj.style.display = "table-row";
    else
        cantHorasRowObj.style.display = "none";


}
