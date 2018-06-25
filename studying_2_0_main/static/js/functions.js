

$(function(){

  $("#id_add_acc").click(function(){              //adds account to project when clicked
    var acc_name = $("#id_account").val();
    $.ajax({
        type: "POST",
        url: "/projects/new_project/add_user",
        data: {
            acc_name: acc_name
        },
        success: function(data) {
          var exists = data.exists
            if(exists != false){
              $(".username").css("color", "green");
              $(".username").text("successfully added user");
              acc_name = acc_name + ', '
              $("#id_accounts").val(($("#id_accounts").val()) + acc_name);
              $("#id_account").val("");
            }
            else{
              $(".username").css("color", "red");
              $(".username").text("user does not exist or is already in your project");
            }
            $(".username").show(800, function(){
              $(".username").hide(800);
            }
          );
        }

      });
    });






});







function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});
