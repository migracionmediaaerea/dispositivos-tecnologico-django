const direccionSelect = document.getElementById('id_direccion');
const jefeSelect = document.getElementById('id_jefe');
const genericOption = document.createElement('option');
const cargoSelect = document.getElementById('id_cargo_foraneo');
genericOption.text = 'Seleccione a un jefe inmediato';

const getJefes = () => {
    // Clean select
    jefeSelect.innerHTML = '';

    // for(let i = 0; i < jefeSelect.options.length; i++) {
    //     jefeSelect.remove(i);
    // }
    jefeSelect.appendChild(genericOption);
    if (direccionSelect.value === '' || cargoSelect.value === '') return;
    result = fetch(`/users/get-jefe/?id=${direccionSelect.value}&cargo=${cargoSelect.value}`)
        .then(response => response.json())
        .then(data => {
            data.forEach(jefe => {
                let option = document.createElement('option');
                option.value = jefe.id;
                option.text = jefe.first_name;
                jefeSelect.appendChild(option);
            });
        })
}

direccionSelect.addEventListener('change', getJefes);
cargoSelect.addEventListener('change', getJefes);