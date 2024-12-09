(function () {
    const addbtn = document.querySelectorAll('.eliminar');
    const csrf_token = document.querySelector("[name='csrf-token']").value;


    addbtn.forEach((btn) => {
        btn.addEventListener('click', function () {

            const isbn = btn.getAttribute('data-isbn');

            confirmarEliminar(isbn);
        })
    });

    const confirmarEliminar= (isbn) => {

        Swal.fire({
            title: '¿Desea continuar con el proceso?',
            inputAttributes: {
                autocapitalize: 'off'
            },
            showCancelButton: true,
            confirmButtonText: 'Eliminar',
            showLoaderOnConfirm: true,
            preConfirm: async () => {
                console.log(window.origin);

                const formData = new FormData();
                formData.append('isbn', isbn);
                
              
                console.log(formData)
                return await fetch(`${window.origin}/delete_book`, {
                    method: 'POST',
                    mode: 'same-origin',
                    credentials: 'same-origin',
                    headers: {
                        'X-CSRF-TOKEN': csrf_token
                    },
                    body: formData,

                    

                    
                }).then(response => {
                    if (!response.ok) {
                        notificacionSwal('Error', response.statusText, 'error', 'Cerrar');
                    }
                    return response.json();
                }).then(data => {
                    if (data.exito) {
                        Swal.fire({
                           position: "Center",
                            titleText: '¡Éxito!',
                            icon: "success",
                            title: "Libro eliminado exitosamente",
                            showConfirmButton: '¡Ok!',
                            timer: 1500
                        }).then((result) => {
                            if (result.dismiss === Swal.DismissReason.timer) {
                                window.location.href = '/index';
                            } else if (result.isConfirmed) {
                                window.location.href = '/index';
                            }
                        });
                    } else {
                        Swal.fire({
                            title: "Error",
                            text: data.mensaje,
                            icon: "warning",
                        });
                    }
                }).catch(error => {
                    Swal.fire({
                        title: "Error",
                        text: error.message,
                        icon: "error",
                    });
                });
            },
            allowOutsideClick: () => false,
            allowEscapeKey: () => false
        });
    };
})();