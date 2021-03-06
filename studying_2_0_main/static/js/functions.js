
var quo = "\'"


function add_account(){              //adds account to project
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

            $("#id_account").val("");
            $(".accounts").append("<li class=" + quo + "account" + quo + "id=" + quo + acc_name + quo + ">" + acc_name + "</li>");
            $("#id_account").append("<input type=" + quo + "hidden" + quo + "id=" +
              quo + acc_name + quo +
              "name=" + quo + "accounts" + quo + "value=" + quo + acc_name + quo + ">");
          }
          else{

          }
      }
    });
  }

function add_tag(){
  var tag_name = $("#id_tag").val();

  $("#id_tag").val("");
  $(".tags").append("<li class=" + quo + "tag" + quo + "id=" + quo + tag_name + quo + ">" + tag_name + "</li>");
  $("#id_tag").append("<input type=" + quo + "hidden" + quo + "id=" +
    quo + tag_name + quo +
    "name=" + quo + "tags" + quo + "value=" + quo + tag_name + quo + ">");



}






$(function(){

  $(document).on('click', ".project_element", function(){

    var element_id = $(this).attr('id');
    var project_id = $(".project_name").attr('id');
    $.ajax({
        type: "GET",
        url: "/projects/" + project_id + "/elements/" + element_id,
        success: function(data) {
          if(document.getElementsByClassName("pdf_field").length == 0) {
              $('.element').append(data);
            }
          else {
            $('.element').empty();
          }

        }

      });
  });

  $(".accounts").on("dblclick", "li", function(){
      var val = $(this).text();
      $(this).remove();
      $("#" + val).remove();


  });


  $(".project_elements").on('click', '.expand' , function(){

    var folder_id = $(this).attr('id');
    var project_id = $(".project_name").attr('id');
    var href = document.location.href;
    var lastPathSegment = href.substr(href.lastIndexOf('/') + 1);
    var detail;

    if(lastPathSegment == 'edit') {
      detail = false;
    }
    else {
      detail = true;
    }

    $.ajax({
        type: "GET",
        url: "/projects/" + project_id + '/' + folder_id,
        data: {
          detail : detail
        },
        success: function(data) {

            if($("#" + folder_id).contents().get(0).nodeValue == '+') {
              expand('#' + folder_id + '_expand', data);
              $("#" + folder_id).text('-');
            }

            else {
              decrease('#' + folder_id + '_container');
                $("#" + folder_id).text('+');
            }


        }

      });


  });

  $("#edit_project").on('change', '.project_elements :checkbox' , function(){

      var check_count = $("input:checked").length;

      if(check_count == 0){
        $("#delete").prop("disabled", true);
        $("#edit").prop("disabled", true);
      }
      else if(check_count == 1){
        $("#delete").prop("disabled", false);
        $("#edit").prop("disabled", false);
      }
      else if(check_count > 1){
        $("#delete").prop("disabled", false);
        $("#edit").prop("disabled", true);
      }

  });





});


function expand(selector, data) {
  $(selector).after(data);
}

function decrease(selector) {
 $(selector).remove();
}











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
