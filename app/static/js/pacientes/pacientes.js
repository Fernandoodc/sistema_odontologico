$(document).ready(function () {
    $('#newFechNac').attr({
        'max': date(),
    });
    $('#pacientes-table').DataTable({
        language: spanish,
    });
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
                            text: item.documento + " - " + item.nombre + " " + item.apellido // Mostrar el nombre completo del repositorio
                        };
                    })
                };
            },
            cache: true
        },
        placeholder: 'Busque un paciente',
        minimumInputLength: 1
    });

});
$('#newPaciente-btn').click(async function (e) {
    e.preventDefault();
    $('#newCita-modal').modal('hide');
    $('#paciente-input').prop('disabled', false)
    $('.infoPaciente').remove();
    $('.paciente-input').prop('disabled', false)
    $('#newPaciente-submit').show();
    $('#newPaciente-submit').html('Guardar');
    $('#pacientes-form')[0].reset()

    //elimina todos los eventos anteriores asociados al form y crea uno nuevo para agregar pacientes
    await $('#pacientes-form').unbind();
    $('#pacientes-form').submit(function (e) {
        e.preventDefault();
        var datos = {
            documento: $('#newDocumento').val(),
            nombre: $('#newNombre').val(),
            apellido: $('#newApellido').val(),
            nacimiento: $('#newFechNac').val(),
            sexo: $('#newSexo').val(),
            estadoCivil: $('#newEstCivil').val(),
            celular: $('#newCelular').val(),
            email: $('#newEmail').val(),
            direccion: $('#newDireccion').val(),
        }
        $.ajax({
            type: "POST",
            url: "/pacientes/nuevo",
            data: JSON.stringify(datos),
            contentType: "application/json",
            dataType: 'json',
            beforeSend: function () {
                $('#newPaciente-submit').html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>');
            },
            success: function (result, textStatus, xhr) {
                //tablaCuentas.ajax.reload(null, false)
                $('#pacientes-form')[0].reset()
                $('#newPaciente-alert').hide();

            },
            complete: function (xhr, textStatus) {
                if (xhr.status == 201)
                    $('#newPaciente-submit').html('Guardar <i class="ri-check-double-fill"></i>');
                else
                    $('#newPaciente-submit').html('Guardar');
            },
            error: function (e) {
                console.log(e)
                if (e.status == 409) {
                    $('#newPaciente-alert').show();
                    $('#newPaciente-alert strong').text(e.responseJSON);
                } else {
                    alert(e.statusText)
                }
            }
        });
    });

    $('#newPaciente-modal').modal('show');
});

$('#newPaciente-modal').on('hidden.bs.modal', function () {
    $('#newCita-modal').modal('show');
});
$('#newPaciente-modal').on('show.bs.modal', function () {
    $('#newPaciente-alert').hide();
});


function cancelUpdate() {
    $('#newPaciente-alert').hide();
    $('.updatePaciente').hide();
    $('#editarPaciente-btn').show();
    $('#deletePaciente-btn').show();
    $('.paciente-input').prop('disabled', true)
}
function rellenarForm(datos) {
    $('#newDocumento').val(datos.documento);
    $('#newNombre').val(datos.nombre);
    $('#newApellido').val(datos.apellido);
    $('#newFechNac').val(datos.nacimiento);
    if (datos.sexo == true) {
        $('#newSexo').val('1').change();
    } else
        $('#newSexo').val('0').change();
    $('#newEstCivil').val(datos.id_ec).change();
    $('#newCelular').val(datos.celular);
    $('#newEmail').val(datos.email);
    $('#newDireccion').val(datos.direccion);
}


async function infoPaciente(idPaciente) {
    //Se reutiliza el modal de nuevo paciete agregando nuevos botones para editar y eliminar
    $('.paciente-input').prop('disabled', true)
    $('.infoPaciente').remove();
    $('#pacientes-modalfooter').append(
        '<button type="button" id="editarPaciente-btn" class="btn btn-primary infoPaciente editarPaciente-btn" title="Editar"><i class="ri-edit-box-line"></i> </button>',
        '<button type="submit" id="updatePaciente-submit" class="btn btn-success updatePaciente-btn updatePaciente infoPaciente" title="Guardar" form="pacientes-form"><i class="ri-save-2-line"></i></button>',
        '<button type="button" id="cancelUpdate-btn" class="btn btn-danger updatePaciente-btn updatePaciente infoPaciente" title="Cancelar"><i class="ri-close-circle-line"></i></button>',
        '<button type="button" id="deletePaciente-btn" class="btn btn-danger updatePaciente-btn infoPaciente" title="Eliminar"><i class="ri-delete-bin-6-line"></i></button>'
    );
    $('#newPaciente-submit').hide();
    $('.updatePaciente').hide();
    $('#newPaciente-modal').modal('show')

    //traemos los datos del paciente y llenamos el form
    var datosPaciente
    $.ajax({
        type: "get",
        url: "/pacientes/info/" + idPaciente,
        success: function (datos) {
            if (datos == null) {
                $('#newPaciente-alert').html('No se pudo recuperar los datos del pacientes');
                return 0
            }
            datosPaciente = datos
            rellenarForm(datos)
        },
        error: function (e) {
            console.log(e)
            $('#newPaciente-alert').html('Ocurrió un error');
        }
    });

    //acciones para boton editar
    await $('#editarPaciente-btn').unbind()
    $('#editarPaciente-btn').click(async function (e) {
        e.preventDefault();
        $('.updatePaciente').show();
        $('#editarPaciente-btn').hide();
        $('#deletePaciente-btn').hide();
        $('.paciente-input').prop('disabled', false)

        //reutilizamos en mismo form para nuevos pacientes eliminando todos los eventos asociados a ella
        await $('#pacientes-form').unbind();
        //agregamos un nuevo evento, que será para actualizar
        $('#pacientes-form').submit(function (e) {
            e.preventDefault();
            var datos = {
                documento: $('#newDocumento').val(),
                nombre: $('#newNombre').val(),
                apellido: $('#newApellido').val(),
                nacimiento: $('#newFechNac').val(),
                sexo: $('#newSexo').val(),
                estadoCivil: $('#newEstCivil').val(),
                celular: $('#newCelular').val(),
                email: $('#newEmail').val(),
                direccion: $('#newDireccion').val(),
            }
            $.ajax({
                type: "put",
                url: "/pacientes/editar/" + idPaciente,
                data: JSON.stringify(datos),
                contentType: "application/json",
                dataType: 'json',
                beforeSend: function () {
                    $('#updatePaciente-submit').html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>');
                },
                success: function (result, textStatus, xhr) {
                    cancelUpdate()
                    $('#newPaciente-alert').hide();
                },
                complete: function (xhr, textStatus) {
                    $('#updatePaciente-submit').html('<i class="ri-save-2-line"></i>');
                },
                error: function (e) {
                    console.log(e)
                    if (e.status == 409) {
                        $('#newPaciente-alert').show();
                        $('#newPaciente-alert strong').text(e.responseJSON);
                    } else {
                        alert(e.statusText)
                    }
                }
            });
        });
    });
    //boton cancelar edicion de pacients
    await $('#cancelUpdate-btn').unbind()
    $('#cancelUpdate-btn').click(function (e) {
        e.preventDefault();
        cancelUpdate()
        rellenarForm(datosPaciente)
    });
    //eliminar paciente
    await $('#deletePaciente-btn').unbind()
    $('#deletePaciente-btn').click(async function (e) {
        e.preventDefault();
        $('#newPaciente-modal').modal('hide')
        $('#deletePaciente-modal').modal('show');
        await $('#eliminar-btn').unbind()
        $('#eliminar-btn').click(function (e) {
            e.preventDefault();
            $.ajax({
                type: "delete",
                url: "/pacientes/eliminar/" + idPaciente,
                success: function (response) {
                    $('#deletePaciente-modal').modal('hide');
                    $('#' + idPaciente).remove();
                },
                error: function (e) {
                    console.log(e)
                    alert(e.statusText)
                }

            });
        });
    });


} 