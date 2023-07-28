$(document).ready(function () {

    $('.pacienteId').select2({
        language: "es",
        dropdownParent: $('#newCita-modal .modal-body'),
        theme: "bootstrap-5",
        ajax: {
            url: '/pacientes/search',
            delay: 250,
            dataType: 'json',
            // Additional AJAX parameters go here; see the end of this chapter for the full code of this example
            processResults: function (data) {
                return {
                    results: data.map(function (item) {
                        return {
                            id: item.id_paciente,
                            text: item.documento + " - " + item.nombre + " " +item.apellido // Mostrar el nombre completo del repositorio
                        };
                    })
                };
            },
            cache: true
        },
        placeholder: 'Busque un paciente',
        minimumInputLength: 1
    });
    /*$('#idDoctor').select2({
        language: "es",
        dropdownParent: $('#newCita-modal .modal-body'),
        theme: "bootstrap-5",
        ajax: {
            url: '/doctores/search',
            delay: 250,
            dataType: 'json',
            // Additional AJAX parameters go here; see the end of this chapter for the full code of this example
            processResults: function (data) {
                return {
                    results: data.doctores.map(function (item) {
                        return {
                            id: item.id,
                            text: item.nombre + " " +item.apellido // Mostrar el nombre completo del repositorio
                        };
                    })
                };
            },
            cache: true
        },
        placeholder: 'Busca un Doctor',
        minimumInputLength: 1

    });*/
});