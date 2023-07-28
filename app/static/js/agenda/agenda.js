$('#newCita-modal').on('show.bs.modal', function (e) {
    //$('.newPaciente-div').hide()
    $('#newCita-alert').hide();
    //$('#newPaciente').prop('checked', false);
})

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



$('#filtrar-citas').click(function (e) {
    e.preventDefault();
    var fecha = $('#desde').val();
    var dr = $('#dr').val();
    if(dr == null || dr == 'null'){
        location.href = '/agenda?' + $.param({ 'fecha': fecha})
    }else
        location.href = '/agenda?' + $.param({ 'fecha': fecha, 'idDoctor': dr })
});