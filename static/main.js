$(document).ready(function () {
    $('#button-modal').hide();
    $('.image-section').hide();
    $('.loader').hide();
    $('#result').hide();

    function read(input) {
        if(input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').css('background-image', 'url('+ e.target.result + ')');
                $('#imagePreview').hide();
                $('#imagePreview').fadeIn(650);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }

    $('#imageUpload').change(function () {
        $('.image-section').show();
        $('#btn-predict').show();
        $('#result').hide();

        read(this);
    });

        $('button.en-th').click( function (){
        var id  = $(this).attr('id');
        var from_data = new FormData($('#upload-file')[0]);
        $('.loader').show();

        $.ajax({
            type: 'POST',
            url: '/predict',
            data: from_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
           if(id == "1" ){
            data = data.TH.slice(0).sort((a,b) => b.accuracy - a.accuracy);
            $(this).hide();

            }
            else if(id == "3"){
               console.log("Go");
               data = data.TH.slice(0).sort((a,b) => b.accuracy - a.accuracy);

            }
            else{
              data = data.EN.slice(0).sort((a,b) => b.accuracy - a.accuracy);
            }
//            data = data.EN.slice(0).sort((a,b) => b.accuracy - a.accuracy);

            console.log(data)
           var total = Object.keys(data).length;
           
            console.log(total)
            var x=""; var type =""; var type_of_string="";var  modal_detail="";

            for( var i = 0; i < total; i++) {
//                  console.log(data['EN']['aid']);

                  symptoms  = data[i].symptoms.split(" ").map(element=>'<br><li>'+ element +'</li>');
                  type_of_string +="<br>"+ data[i].type;

                  modal_detail += "<br>"+data[i].name +"<br>" + "อาการ:   " + symptoms + "<br>" + "การปฐมพยาบาลเบื้องต้น:   "+ data[i].aid+ "<br>" +'<p style="color: '+data[i].colorStyle +'">' +data[i].type+'</p>';


                  x +="<br>"+data[i].name +" ความแม่นยำ: "+ data[i].accuracy +"% " +'<p style="color: '+data[i].colorStyle +'">' +data[i].type+'</p>' ;
//                  el  = $('#mess').css('color', data[i].colorStyle)

            }
               console.log(x);
                $('.loader').hide();
                $('#result').fadeIn(600);
                $('#modal').html(modal_detail);
                $('#result').html(' Result: ' + x);
                $('#button-modal').show();

//                el.html(type_of_string);
                console.log('Success!');

            },

        });

    });


});


