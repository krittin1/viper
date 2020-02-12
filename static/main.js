
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

        $('#btn-predict').click( function (){
        var from_data = new FormData($('#upload-file')[0]);
        $(this).hide();
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
            data = data.slice(0).sort((a,b) => b.accuracy - a.accuracy);
            console.log(data)
            var total = Object.keys(data).length;
            var x="";
            var type ="";
            var type_of_string="";
            var  modal_detail="";

            for( var i = 0; i < total; i++) {
                  type_of_string +="<br>"+ data[i].type;
                  x +="<br>"+data[i].name +" ความแม่นยำ: "+ data[i].accuracy +"% " +'<p style="color: '+data[i].colorStyle +'">' +data[i].type+'</p>';
                  modal_detail += "<br>"+data[i].name +"  อาการ: "+data[i].symptoms+"<br>"+ "การปฐมพยาบาลเบื้องต้น: "+ data[i].aid+"<br>"+'<p style="color: '+data[i].colorStyle +'">' +data[i].type+'</p>';
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

