// metodo para llamar en onChange() del select id region

function getEspSelected() {
    let e = document.getElementById("id_especie");
    let id_esp_selected = e.options[e.selectedIndex].value;
    loadRaces(id_esp_selected);
} //working

// cargar provincias segun región
function loadRaces(id_especie) {
    let api_races_url = `http://fcv.onecloud.cl:8181/ords/fcv_pt/api_razas/races_by_esp?id_especie=${id_especie}`;
    let select = document.getElementById("id_raza");
    select.innerHTML = ''; // clear options

    const blank_op = document.createElement('option');
    blank_op.text = "- Seleccione - ";
    blank_op.setAttribute("disabled", "");
    blank_op.setAttribute("selected", "");
    select.add(blank_op);
    
    fetch(api_races_url)
        .then(response => response.json())
        .then(data => {
            //select.innerHTML = ''; // clear options
            data.items.forEach(item => {
                const option = document.createElement('option');
                option.value = item.id_raza;
                option.text = item.nombre;
                select.add(option);
            });
        })
        .catch(error => {
            alert('Error al cargar razas: ',error);
        })
}
