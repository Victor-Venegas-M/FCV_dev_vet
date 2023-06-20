
// metodo para llamar en onChange() del select id region

function getRegionSelected() {
    let com_select = document.getElementById("comuna");
    com_select.innerHTML = '';
    const blank_op = document.createElement('option');
    blank_op.text = "- Seleccione - ";
    blank_op.setAttribute("disabled", "");
    blank_op.setAttribute("selected", "");
    com_select.add(blank_op);

    let e = document.getElementById("region");
    let id_reg_selected = e.options[e.selectedIndex].value;
    loadProvinces(id_reg_selected);
} //working

// cargar provincias segun región
function loadProvinces(id_region) {
    let api_prov_url = `http://fcv.onecloud.cl:8181/ords/fcv_pt/api_reg_modules/prov_by_reg?id_region=${id_region}`;
    let select = document.getElementById("provincia");
    select.innerHTML = ''; // clear options

    const blank_op = document.createElement('option');
    blank_op.text = "- Seleccione - ";
    blank_op.setAttribute("disabled", "");
    blank_op.setAttribute("selected", "");
    select.add(blank_op);
    
    fetch(api_prov_url)
        .then(response => response.json())
        .then(data => {
            //select.innerHTML = ''; // clear options
            data.items.forEach(item => {
                const option = document.createElement('option');
                option.value = item.id_provincia;
                option.text = item.nombre;
                select.add(option);
            });
        })
        .catch(error => {
            alert('Error al cargar procinvias: ',error);
        })
}



// cargar comunas segun provincia
function getProvinceSelected() {
    let e = document.getElementById("provincia");
    let id_prov_selected = e.options[e.selectedIndex].value;
    loadComunas(id_prov_selected);
}
function loadComunas(id_provincia) {
    let api_com_url = `http://fcv.onecloud.cl:8181/ords/fcv_pt/api_reg_modules/com_by_prov?id_provincia=${id_provincia}`;
    let select = document.getElementById("comuna");

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
                option.value = item.cut;
                option.text = item.nombre;
                select.add(option);
            });
        })
        .catch(error => {
            alert('Error al cargar comunas: ',error);
        })
}

function testCom(){
    let e = document.getElementById("comuna");
    let cut = e.options[e.selectedIndex].value;
    alert(cut);
}


fetch('http://fcv.onecloud.cl:8181/ords/fcv_pt/api_reg_modules/prov_by_reg')