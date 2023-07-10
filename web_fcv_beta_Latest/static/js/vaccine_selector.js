// cargar comunas segun provincia
function getPacienteSelected() {
    let e = document.getElementById("id_paciente");
    let id_paciente = e.options[e.selectedIndex].value;
    loadEspecie(id_paciente);
}

function loadEspecie(id_paciente) {
    let api_com_url = `http://fcv.onecloud.cl:8181/ords/fcv_pt/api_pacientes/paciente?id_paciente=${id_paciente}`;
    let select = document.getElementById("id_especie");

    select.innerHTML = '';
    const blank_op = document.createElement('option');
    blank_op.text = "- Seleccione - ";
    blank_op.setAttribute("disabled", "");
    blank_op.setAttribute("selected", "");
    select.add(blank_op);

    fetch(api_com_url)
        .then(response => response.json())
        .then(data => {
            //select.innerHTML = ''; // clear options
            data.items.forEach(item => {
                const option = document.createElement('option');
                option.value = item.id_especie;
                option.text = item.especie;
                select.add(option);
            });
        })
        .catch(error => {
            alert('Error al cargar especies: ',error);
        })

}

function loadVaccines() {
    let e = document.getElementById("id_especie");
    let id_especie = e.options[e.selectedIndex].value;
    let api_com_url = `http://fcv.onecloud.cl:8181/ords/fcv_pt/api_vacunas/vacs_by_esp?id_especie=${id_especie}`;
    let select = document.getElementById("id_vacuna");

    select.innerHTML = '';
    const blank_op = document.createElement('option');
    blank_op.text = "- Seleccione - ";
    blank_op.setAttribute("disabled", "");
    blank_op.setAttribute("selected", "");
    select.add(blank_op);


    fetch(api_com_url)
        .then(response => response.json())
        .then(data => {
            //select.innerHTML = ''; // clear options
            data.items.forEach(item => {
                const option = document.createElement('option');
                option.value = item.id_vacuna;
                option.text = item.nombre;
                select.add(option);
            });
        })
        .catch(error => {
            alert('Error al cargar vacunas: ',error);
        })
}