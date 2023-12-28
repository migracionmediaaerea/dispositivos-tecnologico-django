

// remitente = document.getElementById("id_remitente");
remitente = $('#id_remitente')

// remitente.addEventListener("input", get_remitentes);


remitente.on('select2:select', function (e) {

    let data = e.params.data;
    get_persona(data.id)
    // Do something
});


// function that call api and get data from remitente
function get_persona(data) {

    if (data == ""){
        return
    }
    const url = "/documentos/get_persona/"  + data;

    fetch(url)
        .then((response) => response.json())
        .then((data) => {
            console.log(data)
            const dependencia = document.getElementById("id_dependencia");
            const cargo = document.getElementById("id_cargo");
            const area = document.getElementById("id_area");
            const domicilio = document.getElementById("id_domicilio");
            if (data.exist == true){
            cargo.value = data.persona.cargo;
            cargo.disabled = true;
            area.value = data.persona.area;
            area.disabled = true;
            domicilio.value = data.persona.domicilio;
            domicilio.disabled = true;

            dependencia.options.length = 0;
            dependencia.options[0] = new Option(data.persona.dependencia, data.persona.dependencia);
            dependencia.value = data.persona.dependencia;
            dependencia.disabled = true;
            }else{
                cargo.value = "";
                cargo.disabled = false;
                area.value = "";
                area.disabled = false;
                domicilio.value = "";
                domicilio.disabled = false;
                dependencia.options.length = 0;
                dependencia.options[0] = new Option("---------", "");
                dependencia.options[1] = new Option("Particular", "Particular");
                dependencia.value = ""
                dependencia.disabled = false;
            }
        }
    );
}


get_persona(remitente.select2('data')[0].id)

