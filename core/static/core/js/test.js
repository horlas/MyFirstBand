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
