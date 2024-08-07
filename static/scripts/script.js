const URL = "http://127.0.0.1:5000/";

        document.getElementById("formulario").addEventListener("submit", function(event) {
            event.preventDefault();

            var datos = new FormData(this);

            fetch(URL + 'login', {
                method: 'POST',
                body: datos
            })
            .then(function (response) {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error('Error al iniciar sesión.');
                }
            })
            .then(function (data) {
                alert('Inicio de sesión exitoso.');
                window.location.href = URL + "profile";
            })
            .catch(function (error) {
                alert('El usuario no existe o la contraseña es incorrecta.');
                window.location.href = URL + "login";
            });
        });
