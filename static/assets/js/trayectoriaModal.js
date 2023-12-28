; (function () {

    const modalTrayectoria = new bootstrap.Modal(document.getElementById('trayectoriaModal'));

    htmx.on("htmx:afterSwap", (e) => {
        if (e.detail.target.id == "dialogTrayectoria") {
            modalTrayectoria.show()
        }
    })

    htmx.on("htmx:beforeSwap", (e) => {
        console.log(e.detail.target.id == "dialogTrayectoria" && !e.detail.xhr.response)
        if (e.detail.target.id == "dialogTrayectoria" && !e.detail.xhr.response) {
            console.log("entro")
            modalTrayectoria.hide()
            e.detail.shouldSwap = false
            console.log(e.detail.xhr.status)
            if (e.detail.xhr.status == 200){
                location.reload()
            }
        }
    })

    htmx.on("hidden.bs.modal", () => {
        document.getElementById("dialogTrayectoria").innerHTML = ""
    })
})();
