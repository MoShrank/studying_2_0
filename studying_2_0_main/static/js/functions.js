var quo = "\'"


function add_account(){              //adds account to project when clicked
  var acc_name = $("#id_account").val();
  $.ajax({
      type: "POST",
      url: "/projects/new_project/add_user",
      data: {
          acc_name: acc_name
      },
      success: function(data) {
        var exists = data.exists
          if(exists != false && !($('#' + acc_name).length > 0)){

      //      $(".username").css("color", "green");
      //      $(".username").text("successfully added user");
            $("#id_account").val("");
            $(".accounts").append("<li class=" + quo + "account" + quo + "id=" + quo + acc_name + quo + ">" + acc_name + "</li>");
            $("#id_account").append("<input type=" + quo + "hidden" + quo + "id=" +
              quo + acc_name + quo +
              "name=" + quo + "accounts" + quo + "value=" + quo + acc_name + quo + ">");
          }
          else{
      //      $(".username").css("color", "red");
      //      $(".username").text("user does not exist or is already in your project");
          }
      //    $(".username").show(800, function(){
      //    $(".username").hide(800);

      //    }
      //  );
      }

    });
  }



$(function(){

  $(".project_element").click(function(){

    var element_id = $(this).attr('id');
    var project_id = $(".project_name").attr('id');
    $.ajax({
        type: "GET",
        url: "/projects/" + project_id + "/elements/" + element_id,
        success: function(data) {
        //    $("#" + element_id).append('<p id=\'' + element_id + '\'>' + data.name + '</p>');
            if($('#' + element_id + '_').length){
              $('#' + element_id + '_').remove();
              $(".pdf_field").attr('src', '');
              $(".pdf_field").hide();
            }
            else{
              $("#" + element_id).append('<p id=\'' + element_id + '_\'>' + data.description + '</p>');
              $(".pdf_field").show();
              $(".pdf_field").attr('src', '/uploads/uploads/pdf.pdf');
            }
        }

      });
  });

  $(".accounts").on("dblclick", "li", function(){
      var val = $(this).text();
      $(this).remove();
      $("#" + val).remove();


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
