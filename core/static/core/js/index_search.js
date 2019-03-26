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
                        //var array = sliceArray(response);
                        var search_text = document.createElement("h5");
                        $(search_text).text("Votre recherche");
                        var divider = document.createElement("div");
                        $(divider).addClass("divider");
                        $('#content').append(search_text);
                        $('#content').append(divider);


                        var cont_card = document.createElement("div");
                        $(cont_card).addClass("grid");
                        $('#content').append(cont_card);


                        $.each(response, function(index, value){
                                if (value.tag =='annonces'){

                                                var card = createCardAds(value);
                                                }
                                if ((value.tag == 'groupes') || (value.tag == 'musicians')) {

                                        var card = createCard(value);
                                        }
                                 $(cont_card).append(card);
                                    });
                                });
               }

// function to create card for announcement
function createCardAds(value){

    var col_card = document.createElement("div");
    $(col_card).addClass('col s3 m4');

    var body_card = document.createElement("div");
    $(body_card).addClass("card custom-bg");

    var card_content = document.createElement("div");
    $(card_content).addClass("card-content");

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
    var url = "/announcement/detail_post/"+value.id;
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

    var card_content = document.createElement("div");
    $(card_content).addClass("card-panel center-align custom-bg ");
    // create img
    var img = createImg(value.avatar);
    card_content.append(img);

    // create card_title
    var title = document.createElement('h5');
    $(title).text(value.name);
    card_content.append(title);

    //create town and county_name
    var local = document.createElement('p');
    $(local).text(value.town + ' ' + value.county_name);
    if (value.tag =='groupes'){
    // create type and musicial genre
    var type_mg = document.createElement('p');
    $(type_mg).text(value.type + ' ' + value.musical_genre);
    $(card_content).append(type_mg);
    //here insert localisation
    $(card_content).append(local);
    // create bio
    var bio = document.createElement('p');
    var short_bio = $.trim(value.bio).substring(0, 100);
    $(bio).text(short_bio+' ...');
    // create link to profile
    var link= linkProfileBand(value.slug);
    bio.append(link);
    $(card_content).append(bio);
    }

    else if (value.tag == 'musicians'){
        $.each(value.instrument, function(index, instru){
        var instrument = document.createElement('p');
        $(instrument).text(instru);
        $(card_content).append(instrument);
        });
        //here insert localisation
        $(card_content).append(local);
        var link= linkProfileMusicians(value.pk);
        $(card_content).append(link);

    }
    return card_content;

}

// function to create img
function createImg(avatar){
    var img = document.createElement('img');
    console.log(avatar);
    if (avatar == 'static/core/img/0_band.jpg'){
        console.log("Yes");
        $(img).attr({
        src: "blblehhh/static/core/img/0_band.jpg",
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

    $(img).attr({
        src: avatar,
        alt: "Avatar",
        class:"circle responsive-img"
        });

    return img
    }

// function to create link profile for "Groupes"
function linkProfileBand(slug){
    var link = document.createElement('a');
    var url = '/core/band_public/'+slug;
    $(link).attr({
        href: url,
        class : "yellow-text"
        });
    $(link).text("   Lire plus");
    return link;
    }

// function to create link profile for Musicians
function linkProfileMusicians(pk){

    var link = document.createElement('a');
    var url = '/core/musician_public/'+pk;
    $(link).attr({
        href: url,
        class : "yellow-text"
        });
    $(link).text("Profil");
    return link;
}