// initialize the select choice //and empty the postal code area
  $(document).ready(function(){
    $('select').formSelect();
    $('#id_cp').val('');
  });


  // function to display results of search form
  function displayResults(){


         // grab data to send
         var item = $('#item').val();
         var cp = $('#id_cp').val();
         // ajax call to grab the data
         $.post(

              "/core/ajax_call/search",
               {'item': item, 'cp': cp},
               function(response){
                        $('#content').empty();
                        var array = sliceArray(response);

                        $.each(array, function(index, row){
                               // var sub_array = row;
                                var cont_card = document.createElement("div");
                                $(cont_card).addClass('row');
                                $.each(row, function(index, value){
                                if (value.tag =='annonces'){

                                                var card = createCardAds(value);
                                                }
                                if ((value.tag == 'groupes') || (value.tag == 'musicians')) {

                                        var card = createCard(value);
                                        }
                                 $(cont_card).append(card);
                                    });
                                $('#content').append(cont_card);
                                });
               });

         };


//function slice in package of three reponse array
function sliceArray(response){
    var new_array = [];
    $.each(response, function(index, value){
        var a = [];
        if (response.length >= 3) {
            for ( i = 0; i <3 ; i++ ){
                a.push(response.pop())};
            new_array.push(a);

        if (response.length < 3){
            new_array.push(response);
            };
            };
            });

    return new_array;
};


// function to create card for announcement
function createCardAds(value){

    var col_card = document.createElement("div");
    $(col_card).addClass('col s3 m4');

    var body_card = document.createElement("div");
    $(body_card).addClass("card custom-bg custom-text");

    var card_content = document.createElement("div");
    $(card_content).addClass("card-content custom-text");

    // create card_title
    var title = document.createElement('span');
    $(title).addClass("card-title");
    $(title).text(value.title);
    card_content.append(title);

    // create local
    var local = document.createElement('p');
    $(local).text(value.town + ' ' + value.county_name);
    card_content.append(local);

    // create created_at
    var time = document.createElement('p');
    $(time).text(value.created_at);
    card_content.append(time);

    // create link
    var cont_link = document.createElement('div');
    $(cont_link).addClass("card-action");
    var link = document.createElement("a");
    var url = "announcement/detail_post/"+value.id;
    $(link).attr({
        href: url,
        });
    $(link).text("Lien vers l'annonce");
    cont_link.append(link);
    card_content.append(cont_link);
    body_card.append(card_content);
    col_card.append(body_card);
    return col_card

}


// function to create cards
function createCard(value){

    var col_card = document.createElement("div");
    $(col_card).addClass('col s3 m4');

    var body_card = document.createElement("div");
    $(body_card).addClass('card');

    var card_img = document.createElement("div");
    $(card_img).addClass('card-image');

    // create img
    var img = createImg(value.avatar);
    card_img.append(img);

    // create card_title
    var title = document.createElement('span');
    $(title).addClass("card-title custom-bg custom-text");
    $(title).text(value.name);
    card_img.append(title);

    if (value.tag =='groupes'){
    // create link to profile
    var link= linkProfileBand(value.slug);
    card_img.append(link);
    }

    if (value.tag =='musicians'){
    // create link to profile
    var link= linkProfileMusicians(value.pk);
    card_img.append(link);
    }

    // create card content
    var card_content = document.createElement("div");
    $(card_content).addClass("card-content custom-bg custom-text");

    if (value.tag =='groupes'){

    // create bio
    var bio = document.createElement('p');
    var short_bio = $.trim(value.bio).substring(0, 100);
    $(bio).text(short_bio+' ...');
    $(card_content).append(bio);
    // create row and divider
    var div = document.createElement('div');
    $(div).addClass("row");
    $(card_content).append(div);
    var divider = document.createElement('div');
    $(div).addClass("divider");
    $(card_content).append(divider);

    // create type and musicial genre
    var type_mg = document.createElement('p');
    $(type_mg).text(value.type + ' ' + value.musical_genre);
    $(card_content).append(type_mg);
    }
    else if (value.tag == 'musicians'){
        $.each(value.instrument, function(index, instru){
        var instrument = document.createElement('p');
        $(instrument).text(instru);
        $(card_content).append(instrument);
        });
        // create row and divider
        var div = document.createElement('div');
        $(div).addClass("row");
        $(card_content).append(div);
        var divider = document.createElement('div');
        $(div).addClass("divider");
        $(card_content).append(divider);
    }

    //create town and county_name
    var local = document.createElement('p');
    $(local).text(value.town + ' ' + value.county_name);
    $(card_content).append(local);
    body_card.append(card_img);
    body_card.append(card_content);
    col_card.append(body_card);
    return col_card;

}

// function to create img
function createImg(avatar){
    var img = document.createElement('img');
    if (avatar == 'static/core/img/0_band.jpg'){
        $(img).attr({
        src: "{% static 'core/img/0_band.jpg' %}",
        alt: "Avatar",
        class:"circle responsive-img"
        });
        }
    else if (avatar == 'static/core/img/0.jpg'){
        $(img).attr({
        src: "{% static 'core/img/0.jpg' %}",
        alt: "Avatar",
        class:"circle responsive-img"
        });

    }
//
//    else {
    $(img).attr({
        src: avatar,
        alt: "Avatar",
        class:"circle responsive-img"
        });

    return img }

// function to create link profile for "Groupes"
function linkProfileBand(slug){
    var ico = document.createElement('i');
    $(ico).addClass("material-icons");
    $(ico).text("add");

    var link = document.createElement('a');
//    var url = '{% url "core:band_profile" 1  %}';
//    var good_url = url.replace('1', slug);
    var url = 'core/band_public/'+slug;
    $(link).attr({
        href: url,
        class : "btn-floating halfway-fab waves-effect waves-light custom-btn-pink"
        });
    link.append(ico);
    return link;
    }

// function to create link profile for Musicians
function linkProfileMusicians(pk){

var ico = document.createElement('i');
    $(ico).addClass("material-icons");
    $(ico).text("add");

    var link = document.createElement('a');
//    var url = '{% url "core:band_profile" 1  %}';
//    var good_url = url.replace('1', slug);
    var url = 'core/musician_public/'+pk;
    $(link).attr({
        href: url,
        class : "btn-floating halfway-fab waves-effect waves-light custom-btn-pink"
        });
    link.append(ico);
    return link;
}