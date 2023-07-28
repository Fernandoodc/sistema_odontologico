$(document).ready(function () {
    $('#motivos-perdida, #elementos_higiene, #causas-falta-trato').select2({
        theme: "bootstrap-5",
    });
    $('.fichaPaciente').prop('disabled', true)
    $(".embarazo-radio, .test-elisa-radio").change(function (e) {
        e.preventDefault();
        var name = $(this).attr("name");
        var selected = $('input[name="' + name + '"]:checked').val();
        var inputDivId = "#" + name + "-inputdiv"
        if (selected == 1) {
            $(inputDivId).show();
        }
        else {
            $(inputDivId).hide();
        }
    });
    $('.check-preguntas').change(function (e) {
        e.preventDefault();
        var checked = $(this).is(':checked')
        var id = $(this).attr('id');
        var inputDivId = '#' + id + '-redDiv'
        $(inputDivId).prop('hidden', !checked);
    });
    getFicha(idPaciente)

    $('#editarFicha-btn, #cargarFicha').click(function (e) {
        e.preventDefault();
        $('.fichaPaciente').prop('disabled', false)
        $('#editarFicha-btn, #cargarFicha').hide()
        $('#ficha-footer').append(`<button type="submit" id="updateFicha-submit"
                class="btn btn-success"
                title="Guardar" form="ficha-form"><i
                    class="ri-save-2-line"></i>
            </button>`,
            `<button type="button" id="cancelUpdate-btn"
                class="btn btn-danger"
                title="Cancelar"><i class="ri-close-circle-line"></i>
            </button>`
        );
        $('#cancelUpdate-btn').unbind();
        $('#cancelUpdate-btn').click(function (e) { 
            e.preventDefault();
            $(this).remove();
            $('#updateFicha-submit').remove();
            $('#editarFicha-btn').show();
            $('.fichaPaciente').prop('disabled', true)
        });

    });
});

/**
 * Extrae el numero de id ubicando en los ID del html, gnralmente usado para enfermedades y preguntas
 * @param {String} texto Texto en formato text-INT-texto o texto-INT, ejemplo preg-45-res, preg-45
 * @returns INT
*/
function extraerId(texto) {
    const partes = texto.split('-');
    if (partes.length >= 2) {
        const numero = partes[1];
        return parseInt(numero)
    } else {
        return null
    }

}

$('#ficha-form').submit(function (e) {
    e.preventDefault();
    preguntas = $('.check-preguntas')
    //respuestas de de las preguntas con check (primera parte de form)
    var respuestas = []
    for (let i = 0; i < preguntas.length; i++) {
        respuestas[i] = {
            idPregunta: extraerId(preguntas[i].id),
            boolRespuesta: preguntas[i].checked
        }
        if (preguntas[i].checked == true) {
            respuestas[i]['textRespuesta'] = $('#' + preguntas[i].id + "-res").val();
        }
    }
    //enfermedades marcadas
    var enfermedades = $('.enfermedades')
    var enfermedadesPaciente = {
        enfermedades: [],
    }
    for (let i = 0; i < enfermedades.length; i++) {
        if (enfermedades[i].checked == true) {
            enfermedadesPaciente['enfermedades'].push({
                idEnfermedad: extraerId(enfermedades[i].id)
            })
        }
    }
    var otraEnfermedad = $('#otroEnf-ficha').val();
    if (otraEnfermedad != '')
        enfermedadesPaciente['otraEnfermedad'] = otraEnfermedad
    //Causas de perdida de dientes
    var causasPerdida = $('#motivos-perdida').val();
    var causasPerdidaPaciente = []
    for (let i = 0; i < causasPerdida.length; i++) {
        causasPerdidaPaciente.push({
            idCausa: parseInt(causasPerdida[i])
        })
    }
    //Causas de falta de trato de los dientes
    var causasFaltaTrato = $('#causas-falta-trato').val();
    var causasFaltaTratoPaciente = {
        causas: []
    }
    for (let i = 0; i < causasFaltaTrato.length; i++) {
        causasFaltaTratoPaciente['causas'].push({
            idCausa: parseInt(causasFaltaTrato[i])
        })
    }
    var otraCausa = $('#otros-causas-falta-trato').val();
    if (otraCausa != '') {
        causasFaltaTratoPaciente['otraCausa'] = otraCausa
    }

    //Elementos que usa el paciente para su higiene bucal
    var elementosHigiene = $('#elementos_higiene').val();
    var elementosHigienePaciente = {
        elementos: [],
    }
    for (let i = 0; i < elementosHigiene.length; i++) {
        elementosHigienePaciente['elementos'].push({
            idElemento: parseInt(elementosHigiene[i])
        })
    }
    var otroElemento = $('#otros_elementos_higiene').val();
    if (otroElemento != '') {
        elementosHigienePaciente['otroElemento'] = otroElemento
    }

    //json a enviar
    var ficha = {
        respuestas: respuestas,
        enfermedades: enfermedadesPaciente,
        causasPerdida: causasPerdidaPaciente,
        causasFaltaTrato: causasFaltaTratoPaciente,
        elementosHigiene: elementosHigienePaciente,
        comentarios: $('#comentarios').val(),
    }

    //Embarazo
    var embarazoCheck = $('input[name="embarazo-radio"]:checked').val();  //el que fue seleccionado
    if (embarazoCheck != undefined) {  //si alguno fue seleccionado
        ficha['embarazo'] = parseInt(embarazoCheck)
        if (embarazoCheck == 1) {
            ficha['tiempoEmbarazo'] = $('#embarazo-tiempo').val();
        }
    }

    //Toleracia a la anestesia
    var anestesiaCheck = $('input[name="anestesia-radio"]:checked').val();
    if (anestesiaCheck != undefined) {
        ficha['toleranciaAnestesia'] = parseInt(anestesiaCheck)
    }

    //Test de Elisa
    var testElisaCheck = $('input[name="test-elisa-radio"]:checked').val();
    if (testElisaCheck != undefined) {
        ficha['testElisa'] = parseInt(testElisaCheck)
        if (testElisaCheck == 1) {
            ficha['tiempoTestElisa'] = $('#test-elisa-tiempo').val();
        }
    }

    //ultima consulta
    var unidadSeleccionada = $('#uni-time-ult-consulta').val();
    var tiempo = parseInt($('#time-ult-consulta').val())
    if (unidadSeleccionada == "anio") {
        ficha['ultimaConsulta'] = tiempo * 12
    } else {
        ficha['ultimaConsulta'] = tiempo
    }
    //Cantidad de cepillado al día
    ficha['cepillado'] = parseInt($('#cant-cepillado').val());
    console.log(ficha)
    $.ajax({
        type: "POST",
        url: "/pacientes/ficha/" + idPaciente,
        data: JSON.stringify(ficha),
        contentType: "application/json",
        dataType: 'json',
        beforeSend: function () {
            $('#updateFicha-submit').html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>');
        },
        success: function (result, textStatus, xhr) {
            console.log(result)
            $('.fichaPaciente').prop('disabled', true);
            $('#alert-ficha').prop('hidden', true);
            $('#cancelUpdate-btn').remove();
            $('#updateFicha-submit').remove();
            $('#editarFicha-btn').show()

        },
        complete: function (xhr, textStatus) {
            $('#updateFicha-submit').html('<i class="ri-save-2-line"></i>');
        },
        error: function (e) {
            console.log(e)
            alert(e.statusText)
        }
    })

});

/**
 * Utilizado para llenar la ficha del paciente con los datos traidos del servidor
 * @param {JSON} datos json con los datos del la ficha recibido del servidor
 * @return {Boolean}
 */
function completarFicha(datos) {
    datos.respuestas.forEach(respuesta => {
        var idCheck = "#preg-" + respuesta.id_pregunta
        $(idCheck + "-redDiv").prop('hidden', !respuesta.bol_respuesta)
        $(idCheck).prop("checked", respuesta.bol_respuesta);
        if (respuesta.text_respuesta) {
            $(idCheck + "-preg").val(respuesta.text_respuesta);
        }

    });
    datos.enfermedades.forEach(enfermedad => {
        $("#enf-" + enfermedad.id_enfermedad).prop("checked", true);
    });
    $('#otroEnf-ficha').val(datos.otro_enfermedad);
    var signNumeros = ['no', 'si', 'nose']  //signigicado de los nuemros devuelto por el server sobre embarazo, tolerancia anestesiam, testElisa. esto según su posición en el array
    $("#embarazo-" + signNumeros[datos.embarazo]).prop("checked", true)
    $('#embarazo-tiempo').val(datos.tiempo_embarazo);
    $("#anestesia-" + signNumeros[datos.tol_anestesia]).prop("checked", true)
    $("#test-elisa-" + signNumeros[datos.test_elisa]).prop("checked", true)
    $('#test-elisa-tiempo').val(datos.tiempo_elisa);
    $('.embarazo-radio, .test-elisa-radio').trigger('change');

    if (datos.ult_consulta % 12 == 0) {
        $('#time-ult-consulta').val(datos.ult_consulta / 12);
        $('#uni-time-ult-consulta').val('anio').change();
    } else {
        $('#time-ult-consulta').val(datos.ult_consulta);
        $('#uni-time-ult-consulta').val('mes').change();
    }
    $('#cant-cepillado').val(datos.cepillado);
    datos.elementosHigiene.forEach(elemento => {
        $('#elementos_higiene option[value="' + elemento.id_elemento + '"]').prop('selected', true);

    });
    $("#elementos_higiene").trigger('change');
    $('#otros_elementos_higiene').val(datos.otro_elemento);
    datos.causasPerdidas.forEach(causa => {
        $('#motivos-perdida option[value="' + causa.id_causa + '"]').prop('selected', true);
    });
    $('#motivos-perdida').trigger('change');
    datos.causasFaltaTrato.forEach(causa => {
        $('#causas-falta-trato option[value="' + causa.id_causa + '"]').prop('selected', true);
    });
    $('#causas-falta-trato').trigger('change');
    $('#otros-causas-falta-trato').val(datos.otro_falta_trato);
    $('#comentarios').val(datos.comentarios);



}

/**
 * Obtiene la ficha del paciente y lo muestra en pantalla
 * @param {INT} idPaciente Id de paciente de quien se quiere obtener la ficha
 */
function getFicha(idPaciente) {
    //$('.fichaPaciente').prop('disabled', true)
    $.ajax({
        type: "get",
        url: "/pacientes/ficha/" + idPaciente,
        /*beforeSend: function () {
            $('#updateFicha-submit').html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>');
        },*/
        success: function (response) {
            if (response == null) {
                $('#alert-ficha').addClass('alert-warning');
                $('#alert-ficha strong').html('El paciente no tiene una ficha cargada');
                $('#alert-ficha').prop('hidden', false)
                $('#cargarFicha').show();
                return 0
            }
            else {
                $('#alert-ficha').prop('hidden', true)
                completarFicha(response)
            }
            console.log(response)
        },
        error: function (e) {
            console.log(e)
            $('#alert-ficha').addClass('alert-danger');
            $('#alert-ficha strong').html('Ocurrió un error');
            $('#cargarFicha').hide();
            $('#alert-ficha').prop('hidden', false)
        }
    });
}