$(document).ready(function() {

    $.ajax({
        url: "static/data.json",
        dataType: "json"
    }).done(function(response) {
        console.log(response);
        var x="";
        response.forEach(element => {
            console.log(element.name, element.size, element.nature, element.reproduction, element.food
                , element.habitat, element.spread, element.symptom, element.aid, element.treatment, element.image);

              x +="<div><h2>"+
             element.name + "</h2></div>" +
              "<p><b>ขนาด </b>"  + element.size + "</p>" +
              "<p><b>ลักษณะ </b>"  + element.nature + "</p>" +
              "<p><b>การสืบพันธุ์ </b>"  + element.reproduction + "</p>" +
              "<p><b>อาหาร </b>"  + element.food + "</p>" +
              "<p><b>แหล่งที่พบ </b>"  + element.habitat + "</p>" +
              "<p><b>การแพร่กระจาย </b>"  + element.spread + "</p>" +
              "<p><b>อาการ </b>"  + element.symptom + "</p>" +
              "<p><b>การปฐมพยาบาล </b>"  + element.aid + "</p>" +
              "<b>การรักษา </b>"  + element.treatment + "</p>"  +
              '<div class="search-image">'+
                                    '<img style="high: 350px;width: 350px;" src="'+ element.image +'">'+
                                '</div>';

             $('#teety').html(x);


        });
    });
});





$('#submit-btn').click(function(){
    console.log($('#input-text').val());
    $.ajax({
        url: "static/data.json",
        dataType: "json"
    }).done(function(response) {
        console.log(response);
        var x="";
        if($('#input-text').val() == ""){ 
            response.forEach(element => {                      
                console.log(element.name, element.age, element.brand, element.color, element.model, element.price);
                x +="<h1>"+
             element.name + "</h1>" +
              "<p><b>ขนาด </b>"  + element.size + "</p>" +
              "<p><b>ลักษณะ </b>"  + element.nature + "</p>" +
              "<p><b>การสืบพันธุ์ </b>"  + element.reproduction + "</p>" +
              "<p><b>อาหาร </b>"  + element.food + "</p>" +
              "<p><b>แหล่งที่พบ </b>"  + element.habitat + "</p>" +
              "<p><b>การแพร่กระจาย </b>"  + element.spread + "</p>" +
              "<p><b>อาการ </b>"  + element.symptom + "</p>" +
              "<p><b>การปฐมพยาบาล </b>"  + element.aid + "</p>" +
              "<b>การรักษา </b>"  + element.treatment + "</p>"  +
              '<div class="search-image">'+
                                    '<img style="high: 350px;width: 350px;" src="'+ element.image +'">'+
                                '</div>';

             $('#teety').html(x);
    
            });
        }
        else{
            response.forEach(element => {                      
                if(element.name.includes($('#input-text').val())  ){
                 x +="<h1>"+
             element.name + "</h1>" +
              "<p><b>ขนาด </b>"  + element.size + "</p>" +
              "<p><b>ลักษณะ </b>"  + element.nature + "</p>" +
              "<p><b>การสืบพันธุ์ </b>"  + element.reproduction + "</p>" +
              "<p><b>อาหาร </b>"  + element.food + "</p>" +
              "<p><b>แหล่งที่พบ </b>"  + element.habitat + "</p>" +
              "<p><b>การแพร่กระจาย </b>"  + element.spread + "</p>" +
              "<p><b>อาการ </b>"  + element.symptom + "</p>" +
              "<p><b>การปฐมพยาบาล </b>"  + element.aid + "</p>" +
              "<b>การรักษา </b>"  + element.treatment + "</p>"  +
              '<div class="search-image">'+
                                    '<img style="high: 350px;width: 350px;" src="'+ element.image +'">'+
                                '</div>';

             $('#teety').html(x);

                }
                
            
    
            });
        }
    });
})



    