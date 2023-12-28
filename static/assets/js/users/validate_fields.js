const curp = document.getElementById('id_curp');
const email = document.getElementById('id_email');
const area = document.getElementById('id_area');
const numeroOficio = document.getElementById('id_numero_oficio');
const nombre = document.getElementById('id_first_name');

const validateEmoji = (e) => {
    const regexEmoji = /(\p{Emoji_Presentation}|\p{Extended_Pictographic})/gu;
    if (regexEmoji.test(e.target.value)) {
        e.target.setCustomValidity('No se permiten emojis');
        e.target.reportValidity();
    }else{
        e.target.setCustomValidity('');
    }
}

const validateAlphanumeric = (e) => {
    const regexLetters = /^[a-zA-ZÀ-ÿ\u00f1\u00d1\s0-9]{1,40}$/;
    if (!regexLetters.test(e.target.value)) {
        e.target.setCustomValidity('Solo se permiten letras');
        e.target.reportValidity();
    }else{
        e.target.setCustomValidity('');
    }
}

const validateString = (e) => {
    const regexLetters = /^[a-zA-ZÀ-ÿ\u00f1\u00d1\s]{1,40}$/;
    if (!regexLetters.test(e.target.value)) {
        e.target.setCustomValidity('Solo se permiten letras');
        e.target.reportValidity();
    }else{
        e.target.setCustomValidity('');
    }
}

const validateWhitespace = (e) => {
    const regexWhitespace = /^\s+$/;
    if (regexWhitespace.test(e.target.value)) {
        e.target.setCustomValidity('No se permiten espacios en blanco');
        e.target.reportValidity();
    }else{
        e.target.setCustomValidity('');
    }
}
// Nombre validations
nombre.addEventListener('input', validateEmoji);
nombre.addEventListener('input', validateAlphanumeric);
// End validations


// Area validations
area.addEventListener('change', validateEmoji);
area.addEventListener('change', validateAlphanumeric);
// End validations


// Numero oficio validations
// numeroOficio.addEventListener('change', validateEmoji);
// numeroOficio.addEventListener('change', validateAlphanumeric);
// numeroOficio.addEventListener('change', validateWhitespace);
// End validations


// Curp validations
curp.addEventListener('change', (e) => {
    // To uppercase whole string
    e.target.value = e.target.value.toUpperCase();
});
curp.addEventListener('change', validateEmoji);
curp.addEventListener('change', validateAlphanumeric);
// End validations


// Email validations
email.addEventListener('change', validateEmoji);
email.addEventListener('change', validateAlphanumeric);
email.addEventListener('change', (e) => {
    // Regex to validate email
    const regex = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    if (!regex.test(e.target.value)) {
        e.target.setCustomValidity('Correo electrónico inválido');
        e.target.reportValidity();
    } else {
        e.target.setCustomValidity('');
    }
    
});
// End validations