$("#first").click(function() {

  $("#first").hide();
  $("#cp").show();
  //$("#btn_send").show();
  //empty id_code
  $('#id_code').val('');


  $("#send").click(function () {

      var $code = $('#id_code').val();

      // valid cp code
      var $return = validateZip($code);
      if ($return === true) {
          var url = createURL($code);
          $.getJSON(
              url,
              function (data) {

                    if (data.length != 0){
                         $.each(data, function (index, value) {
                            $("#id_town").append($("<option value=\"" +value.nom+ "\">" + value.nom + "</option>"));
                                $(document).ready(function () {
                                $('select').formSelect();
                                 });

                             $('#id_county_name').val(value.departement.nom);

                            });
                         $("#send").hide();
                            $("#town").show();
                          } else {
                             // show the modal
                              options is not defined

              });

      } else {
          // show the modal
          var elem = document.querySelector('.modal');
          var instance = M.Modal.init(elem);
          instance.open();
      }

        });
});

//validate postal code

function validateZip(code){
	return (code.length!=5 || isNaN(code)) ? false : true;
}

//create an url
function createURL(code) {
    var baseURL = "https://geo.api.gouv.fr/communes?codePostal="
    var params = {
                    fields : 'nom,departement',
                    format : 'json',
                    geometry : 'centre'
        };
    return(baseURL+code+'&'+ $.param( params ))
}

// initialize the select choice
  $(document).ready(function(){
    $('select').formSelect();
  });

// script to display list of instrument in order to delete just one

$("#delete").click(function() {
    $('#trigger_button').hide();
    $('#form_delete').show();


    })

$("#add").click(function() {
    $('#trigger_button').hide();
    $('#form_add').show();
    })