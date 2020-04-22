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
        console.log("Hrhrhre")
        var id  = $(this).attr('id');
        console.log(id)
        var from_data = new FormData($('#upload-file')[0]);
        console.log(from_data)
        $('.loader').show();
        
        $.ajax({
            type: 'POST',
            url: '/predict',
            data: from_data,
            contentType: false,
            dataType: 'image/jpg',
            cache: false,
            processData: false,
            async: true,
            // data: JSON.stringify(from_data),
            success: function (data) {
            console.log(data)
           if(id == "1" ){
            data = data.TH.slice(0).sort((a,b) => b.accuracy - a.accuracy);
            $(this).hide();

            }
            else if(id == "3"){
//               console.log("Go");
               data = data.TH.slice(0).sort((a,b) => b.accuracy - a.accuracy);

            }
            else{
              data = data.EN.slice(0).sort((a,b) => b.accuracy - a.accuracy);
            }
//            data = data.EN.slice(0).sort((a,b) => b.accuracy - a.accuracy);

//            console.log(data)

//           console.log(total)
          var  key = data;
           var total = Object.keys(data).length;
            console.log(key)
            var x=""; var type =""; var type_of_string="";var  modal_detail="";

            for( var i = 0; i < total; i++) {
//                  console.log(data['EN']['aid']);
                  console.log(key)
                  symptoms  = data[i].symptoms.split(" ").map(element=>'<br><li>'+ element +'</li>');
                  type_of_string +="<br>"+ data[i].type;

                  modal_detail += "<br>"+data[i].name +"<br>" + Object.keys(key[0])[1]+" "+ symptoms + "<br>" + Object.keys(data[0])[4]+" :"+data[i].aid+ "<br>" +'<p style="color: '+data[i].colorStyle +'">' +data[i].type+'</p>';


                  x +="<br>"+data[i].name +" "+ Object.keys(key[0])[0] +": "+ data[i].accuracy +"% " +'<p style="color: '+data[i].colorStyle +'">' +data[i].type+'</p>' ;
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
            error: function(data){
                console.log("error");
                console.log(data);
            },
            timeout: 3000 // sets timeout          

        });

    });


});


