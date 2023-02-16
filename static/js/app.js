let cookie = document.cookie
    token = cookie.split('=')[1]


// Agregar producto al Carrito 'market.html' //
function addCard(id, type){

    console.log(id)
    $.ajax({
        url : '/add-card',
        type : 'post',
        dataType : 'json',
        data : {
            id : id,
            type : type,
            csrfmiddlewaretoken : token,
        }
    })
    .done(function(result){

        if(result.status == false){
            window.location.href = "login-register" 
        }
        else{
            $(".card-container").load(window.location + ' .items-container')
            $("#navbar").load(window.location + " .header")    
        }

        
    })
}


// Registrarse 'login_register.html' //
function registerUser(event){
    event.preventDefault()
    let username = $("#name").val()
    let email = $("#email").val()
    let password1 = $("#password1").val()
    let password2 = $("#password2").val()
    
    $.ajax({
        url : '/login-register',
        type : 'post',
        dataType : 'json',
        data : {
            username : username,
            email : email,
            password1 : password1,
            password2 : password2,
            csrfmiddlewaretoken : token
        }
    })
    .done(function(result){
        if (result.status == false){
            alert('Hubo fallas al registrarse porfavor vuelva a intentar')
            window.location.href = "login-register"
            
        } 
        else {
            window.location.href = "market-place"
        }
    })
}


// Log in 'login_register.html' //
function loginUser(event){
    event.preventDefault()
    let email = $("#email1").val()
    let password = $("#password").val()
    
    $.ajax({
        url : '/login-session',
        type : 'get',
        dataType : 'json',
        data : {
            email : email,
            password : password,
            csrfmiddlewaretoken : token
        }
    })
    .done(function(result){
        if(result.status == false){
            $(".form-session")[0].reset();
            // $(".login-card").load(window.location + ' .form-session')
            alert(result.message)
        } else {
        window.location.href = "market-place"
        }
    })
}