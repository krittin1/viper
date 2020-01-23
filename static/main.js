
$(document).ready(function () {

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
        $('#result').text('');
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
            var x=""
            for( var i = 0; i < total; i++) {
                  x +="<br>"+data[i].name +" ความแม่นยำ: "+ data[i].accuracy +"%" ;
//                console.log("ID: " + data[i].name + " Message " + data[i].accuracy);
            }

             $('.loader').hide();
                $('#result').fadeIn(600);
                $('#result').html(' Result: ' + x);
                console.log('Success!');
            },

        });
    });
});

