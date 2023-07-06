$('#newCita-modal').on('shown.bs.modal', function (e) {
    $('.newPaciente-div').hide()
    $('#newCita-alert').hide();
    $("#newPaciente-form").trigger("reset");
    $('#newPaciente').prop('checked', false);
})

$('#newPaciente').change(function (e) { 
    e.preventDefault();
    var newPaciente = $(this)
    if(newPaciente.is(':checked') == true){
        $('.newPaciente-div').show()
    }
    else{
        $('.newPaciente-div').hide()
    }
});

$('#newCita-form').submit(function (e) { 
    e.preventDefault();
    $('#newCita-submit').prop('disabled', true)
    if ($('#tDuracion').val() == 'min')
        var duracion = $('#duracion').val()
    else
        var duracion = $('#duracion').val() * 60
    var datos = {
        "idPaciente": $('#pacienteId').val(),
        "idDoctor": $('#idDoctor').val(),
        "fecha": $('#fecha').val(),
        "hora": $('#hora').val(),
        "duracion": duracion
    }
    console.log(datos)
    $.ajax({
        type: "POST",
        url: "/agenda/citas/nuevo",
        data: JSON.stringify(datos),
        contentType: "application/json",
        dataType: 'json',
        success: function (result, textStatus, xhr) {
            //tablaCuentas.ajax.reload(null, false)
            console.log(result)
            $('#newCita-form')[0].reset()
            $('#newPaciente').prop('checked', false);
            $('#newCita-alert').hide();
        },
        complete: function (xhr, textStatus) {
            $('#newCita-submit').prop('disabled', false)
        },
        error: function (e) {
            console.log(e)
            if (e.status == 409) {
                $('#newCita-alert').show();
                $('#newCita-alert strong').text(e.responseJSON);
            } else {
                alert(e.statusText)
            }
        }
    });
});

$('#tDuracion').change(function (e) { 
    e.preventDefault();
    if($(this).val() == 'hr')
        $('#duracion').val(1);
    else
    $('#duracion').val(30);
});