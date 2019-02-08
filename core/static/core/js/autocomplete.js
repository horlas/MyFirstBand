$(function() {
            $.ajax({
                url: "{% url 'band:search' %}",
                type: "GET",
                dataType: "json",

                success: function( response ){
                    var userList = response;
                    var dataUser = {};
                    for (var i = 0; i < userList.length; i++) {
                        dataUser[userList[i].value] = null; //countryArray[i].flag or null
                    }
                console.log(dataUser);
                $('#id_musician').autocomplete({
                     data : dataUser,
                     minLength: 2,
                     });
               }
             });
            });