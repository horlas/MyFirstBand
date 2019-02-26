
$("#answer").click(function() {

  $("#response").show();
  $("#answer").hide();
  //empty answer area
   $('#answer_text').val('');

  });

  // to manage textarea count lenght
   $(document).ready(function() {
      $('textarea#answer_text').characterCounter();
    });

