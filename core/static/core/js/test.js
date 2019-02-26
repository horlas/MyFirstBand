function initMessage(object_message){
    console.log(object_message);
    var data = object_message;

        //ajax call to grab all message witch depends on a announcement
        $.post(
                "{% url 'announcement:message_search' %}",
                {'announcement' : data},
                function(response){
                        $.each(response, function(index, value){
                                var $mes = $('<div class='message'></div>');
                                $('#message_list').append($mes);
                                $(".message").text(value);

                                console.log(value);
                                });

                    console.log(response);



                    });

                    }




function addRecordMess(message) {
    var $mes = $('<div class='message'>message</div>').text(message);
    var $mes_zone = $('#message_list').append($mes);
    }


var $link_author = $('<a href="{% url 'core:musician_profile' author_useprofile_id  %}' class="custom-text-link-login ">author</a>");

var $link_author = $('<a href="" class="custom-text-link-login ">author</a>');
var $url = "{% url 'core:musician_profile' author_useprofile_id  %}"





   // function witch get object

    function initMessage(object_message){
       // empty message's zone
       $( "#message_list" ).empty();
       var data = object_message;




           //ajax call to grab all message witch depends on a announcement
           $.post(
                   "{% url 'announcement:message_search' %}",
                   {'announcement' : data},
                   function(response){
                           $.each(response, function(index, value){
                                  addRecordMess(value);
                                   console.log(value);
                                   });

                       });
                       }

   // function to add record message
   function addRecordMess(message) {
       var $mes = $('<div class="message">message</div>').text(message);
       var $mes_zone = $('#message_list').append($mes);
       }


// function witch display received messages
    function displayMessages(content, author, author_useprofile_id){
        $("#message_published_ads_list").empty();
        var $mes = $('<div class="message">message</div>').text(content);
        var $mes_zone = $('#message_published_ads_list').append($mes);
        var $link_author = $('<a href="" class="custom-text-link-login ">author</a>').text(author);
        // to remove white space before variable ?
        var $profile_id = $.trim(author_useprofile_id);
        // because we can not get the userprofile id inside the rendered url
        // we must replace it , initial with a dummy number '1'
        var $url = '{% url "core:musician_profile" 1  %}';
        var $good_url = $url.replace('1', $profile_id);
        $link_author.attr("href", $good_url);
        var $mes_zone = $('#message_published_ads_list').append($link_author);
        }