
document.getElementById("formulario").addEventListener("submit", function(event) {
    event.preventDefault();
    var datos = new FormData(this);
    console.log(datos) 
    
})

