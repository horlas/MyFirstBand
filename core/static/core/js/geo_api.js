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
                              var elem = document.querySelector('.modal');
                              var instance = M.Modal.init(elem);
                              instance.open();
                               }

              });

      } else {
          // show the modal
          var elem = document.querySelector('.modal');
          var instance = M.Modal.init(elem);
          instance.open();
      }


        });
//});

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

// initialize the select choice //and empty the postal code area
  $(document).ready(function(){
    $('select').formSelect();
    $('#id_code').val('');
  });

// script to display list of instrument in order to delete just one
// used for update_musician_profile

$(".delete").click(function() {
    $('.hidden_onclick').hide();
    $('#form_delete').show();


    })

$(".add").click(function() {
    $('.hidden_onclick').hide();
    $('#form_add').show();
    })