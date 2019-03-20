// function witch get object
   // function witch display received messages
    function displayMessages(content, author, author_useprofile_id, id, ads, target, zone_message, signal, author_first_response){
        $(target).empty();
        $(zone_message).show();


       // add first message
        var $mes = $('<div class="message">message</div>').html(content);
        var $mes_zone = $(target).append($mes);
        var $link_author = createLinkAuthor(author, author_useprofile_id);
        var $mes_zone = $(target).append($link_author);

        // add response to this message
        var parent_id = id;
        //ajax call to grab all message witch depends of a parent_id
           $.post(
                   "/announcement/ajax_calls_message/search",
                   {'parent_message' : parent_id},
                   function(response){
                           $.each(response, function(index, value){
                                   var $mes = $('<div class="message">message</div>').html(value.content);
                                   $(target).append($mes);
                                   var $link_author = createLinkAuthor(value.author, value.author_userprofile_id, value.created_at);
                                   $(target).append($link_author);
                                   });
                       });

       // THIS  IS IMPORTANT // to prevent response to this message we pass the parent_id and parent_ads in the answer_zone
        var $parent_id = $('<input type="hidden" name="m_id" value="">');
        $parent_id.attr("value", id);
        var $parent_ads = $('<input type="hidden" name="m_ads" value="">');
        $parent_ads.attr("value", ads);

        var $parent_recipient = $('<input type="hidden" name="m_recipient" value="">');
        // the signal differs between the two type of messages to manage the name of the author
        if (signal==1){
            $("#recipient").text("Vous répondez à "+author_first_response);
            $parent_recipient.attr("value", author_first_response);
            //console.log(author_first_response);
            }
        if (signal==2){
            $("#recipient").text("Vous répondez à "+author);
            $parent_recipient.attr("value", author);
            }

        // empty before to prevent several add on click
        $('#pass_info').empty();
        $('#pass_info').append($parent_id);
        $('#pass_info').append($parent_ads);
        $('#pass_info').append($parent_recipient);
        $('html,body').animate({scrollTop: $('#response').offset().top}, "slow");

        }


   // function to create link to author profile

   function createLinkAuthor(author, author_userprofile_id, date_message){
        var $link_author = $('<a href="" class="custom-text-link-login">author</a>').text(author+' le '+ date_message);
        var $url = '/core/musician_public/'+author_userprofile_id;
        $link_author.attr("href", $url);
        return $link_author;
        }


   // function to manage response to received messages

   function answerMessage(){
    $(".trigger_message").hide();
    $("#response").show();
    }

   $("#answer_message").click(function() {

   $("#response_to_message").show();
   $("#answer_message").hide();
   //empty answer area
   $('#message_text').val('');

   });

   // to manage textarea count lenght
   $(document).ready(function() {
      $('textarea#message_text').characterCounter();
    });