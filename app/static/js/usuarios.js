USERID = ''

async function infoUser(id){
    $('#newPasw').val('');
    $('#reNewPasw').val('');
    $('#alertnewPasw').prop('hidden', true)
    $('.newPasw').css('border-color', '');
    $('#newType-ok').prop('hidden', true)
    $('#newPasw-ok').prop('hidden', true)
    $('#alertPaswLen').prop('hidden', true)
    await $.ajax({
        type: "GET",
        url: "/usuarios/info?"+ $.param({"id": id}),
        success: function(result, textStatus, xhr) { 
            USERID = result.usuario.id
            $('#editar-btn').prop('hidden', false)
            $('#guardarCambios-btn').prop('hidden', true)
            $('#alertUsername').prop('hidden', true)
            $('.obli').prop('hidden', true)
            $('.infoUser').prop('disabled', true)
            $('#editar-btn').prop('hidden', false)
            $('#newUsername').val(result.usuario.username);
            $('#documento').val(result.usuario.documento);
            $('#nombre').val(result.usuario.nombre);
            $('#apellido').val(result.usuario.apellido);
            $('#celular').val(result.usuario.celular);
            $('#email').val(result.usuario.email);
            $('#direccion').val(result.usuario.direccion);
            for(i = 0 ; i< result.permisos.length ; i++){
                document.getElementById(result.permisos[i].codigo).checked = true;
                //$('#'+result.permisos[i].codigo).prop( "checked", true )
            }
            $('#infoUser-modal').modal('show')
        },
        complete: function(xhr, textStatus){
        },
        error: function(e){
            console.log(e)
            alert(e.statusText)
        }
    });
}

$('#editar-btn').click(function (e) { 
    e.preventDefault();
    $('.infoUser').prop('disabled', false)
    $('#editar-btn').prop('hidden', true)
    $('#guardarCambios-btn').prop('hidden', false)
    $('.obli').prop('hidden', false)
});
$('#eliminarUser').click(function (e) { 
    e.preventDefault();
    $('#infoUser-modal').modal('hide')
    $('#eliminarUser-modal').modal('show')
});
$('#eliminar-btn').click(async function (e) { 
    e.preventDefault();
    $('#eliminar-btn').prop('disabled', true)
    await $.ajax({
        type: "DELETE",
        url: "/usuarios/eliminar?"+$.param({'id': USERID}),
        success: function(result, textStatus, xhr) { 
            $('#'+USERID).remove();
            $('#eliminarUser-modal').modal('hide')
        },
        complete: function(xhr, textStatus){
            $('#eliminar-btn').prop('disabled', false)
        },
        error: function(e){
            console.log(e)
            alert(e.statusText)
        }
    });
});

$('#guardarCambios-btn').click(async function (e) { 
    $('#newUsername').css('border-color', '');
    e.preventDefault();
    var username = $('#newUsername')
    var documento = $('#documento')
    var nombre = $('#nombre')
    var apellido = $('#apellido')
    if(username.val() == ''){
        username.focus()
        return 0
    }
    if(documento.val() == ''){
        documento.focus
        return 0
    }
    if(nombre.val() == ''){
        nombre.focus()
        return 0 
    }
    if(apellido.val() == ''){
        apellido.focus()
        return 0
    }
    console.log(1)
    var datos = {
        username: username.val(),
        documento: documento.val(),
        nombre: nombre.val(),
        apellido: apellido.val(),
        celular : $('#celular').val(),
        email: $('#email').val(),
        direccion: $('#direccion').val(),
    }
    console.log(datos)
    $('#guardarCambios-btn').prop('disabled', true)
    await $.ajax({
        type: "PUT",
        url: "/usuarios/editar?"+$.param({'id': USERID}),
        data: JSON.stringify(datos),
        contentType: "application/json",
        dataType: 'json',
        success: function(result, textStatus, xhr) { 
            infoUser(USERID)
        },
        complete: function(xhr, textStatus){
            $('#guardarCambios-btn').prop('disabled', false)
        },
        error: function(e){
            console.log(e)
            if(e.status == 409){
                $('#alertUsername').prop('hidden', false)
                $('#newUsername').css('border-color', '#dc3545');
            }else
                alert(e.statusText)
        }
    });

});
$('#newUsername').keyup(function (e) { 
    e.preventDefault();
    var newUsername = $('#newUsername').val()
    setTimeout(async () => {
        await $.ajax({
            type: "GET",
            url: "/usuarios/verif_username?"+ $.param({"username": newUsername, 'id': USERID}),
            success: function(result){
                $('#alertUsername').prop('hidden', true)
                $('#newUsername').css('border-color', '');
            },
            error: function(e){
                console.log(e)
                if(e.status == 409){
                    $('#alertUsername').prop('hidden', false)
                    $('#newUsername').css('border-color', '#dc3545');
                }else
                    alert(e.statusText)
            }
        })
    }, 1500);

});

$('#guardarTypeUser-btn').click(async function (e) { 
    e.preventDefault();
    $(this).prop('disabled', true)
    $('#newType-ok').prop('hidden', true)
    permisos = $('.checkPermisos')
    console.log(permisos)
    var listPermisos = []
    for(i = 0 ; i < permisos.length ; i++)
        if(permisos[i].checked == true)
            listPermisos.push({
                'codigo': permisos[i].value
            })
    await $.ajax({
        type: "PUT",
        url: "/usuarios/change_type_user?"+ $.param({'idUser': USERID}),
        data: JSON.stringify(listPermisos),
        contentType: "application/json",
        dataType: 'json',
        success: function(result){
            $('#newType-ok').prop('hidden', false)
        },
        complete: function(xhr, textStatus){
            $('#guardarTypeUser-btn').prop('disabled', false);  
        },
        error: function(e){
            console.log(e)
            if(e.status == 409){
                $('#alertUsername').prop('hidden', false)
                $('#newUsername').css('border-color', '#dc3545');
            }
            else
                alert(e.statusText)
        }
    })
});

$('#resetPasw-btn').click(async function (e) { 
    e.preventDefault();
    if(verificarPaswLen() == false || verificarPaswEq() == false){
        return 0
    }
    $(this).prop('disabled', true)
    var datos ={
        userId: USERID,
        newPassword : $('#newPasw').val()
    }
    await $.ajax({
        type: "PUT",
        url: "/usuarios/reset_password",
        data: JSON.stringify(datos),
        contentType: "application/json",
        dataType: 'json',
        success: function(result, textStatus, xhr) { 
            $('#newPasw').val('')
            $('#reNewPasw').val('')
            $('#newPasw-ok').prop('hidden', false)
        },
        complete: function(xhr, textStatus){
            $('#changePasw-btn').prop('disabled', false);
            
        },
        error: function(e){
            console.log(e)
            alert(e.statusText)
        }
    });
});
$('#changePasw-btn').click(async function (e) { 
    e.preventDefault();
    if(verificarPaswLen() == false || verificarPaswEq() == false){
        return 0
    }
    $(this).prop('disabled', true)
    var datos ={
        userId: USERID,
        newPassword : $('#newPasw').val(),
        curretPasw : $('#currentPassword').val()
    }
    await $.ajax({
        type: "PUT",
        url: "/usuarios/act_password",
        data: JSON.stringify(datos),
        contentType: "application/json",
        dataType: 'json',
        success: function(result, textStatus, xhr) { 
            $('#newPasw').val('')
            $('#reNewPasw').val('')
            $('#newPasw-ok').prop('hidden', false)
        },
        complete: function(xhr, textStatus){
            $('#changePasw-btn').prop('disabled', false);
            
        },
        error: function(e){
            console.log(e)
            if(e.status == 400){
                alert(e.responseJSON.msg)
                $('#currentPassword').focus()
            }
        }
    });
});
$('#form-newUSer').submit(async function (e) { 
    e.preventDefault();
    if(verificarPaswLen == false || verificarPaswEq() == false){
        return 0
    }
    $(this).prop('disabled', true)
    var data = {
        username : $('#newUsername').val(),
        password: $('#newPasw').val(),
        documento: $('#documento').val(),
        nombre: $('#nombre').val(),
        apellido: $('#apellido').val(),
        celular: $('#celular').val(),
        email: $('#email').val(),
        direccion: $('#direccion').val(),
    }
    var listPermisos = []
    permisos = $('.checkPermisos')
    console.log(permisos)
    for(i = 0 ; i < permisos.length ; i++)
        if(permisos[i].checked == true)
            listPermisos.push({
                'codigo': permisos[i].value
            })
    data['permisos'] = listPermisos
    console.log(data)
    await $.ajax({
        type: "POST",
        url: "/usuarios/new_user",
        data: JSON.stringify(data),
        contentType: "application/json",
        dataType: 'json',
        success: function(result, textStatus, xhr){
            $('#newUser-ok').prop('hidden', true)
            location.reload()
        },
        complete: function(xhr, textStatus){
            $('#form-newUSer').prop('disabled', true)
            
        },
        error: function(e){
            console.log(e)
            alert(e.statusText)
        }
    });
});


