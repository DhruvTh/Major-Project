var switchStatus = false;
$("#togBtn").on('change', function() {
    switchStatus = $(this).is(':checked');
        // alert(switchStatus);// To verify
    var processing = 'low'
    if(switchStatus == true){
        processing = 'high'
    }
    // alert(processing)
    $('#processing').val(processing)

    document.getElementById("form-id").submit();

});

var switchStatus = false;
$("#togBtn1").on('change', function() {
    switchStatus = $(this).is(':checked');
        // alert(switchStatus);// To verify
    var cap1 = '0'
    if(switchStatus == true){
        cap1 = '1'
    }
    // alert(processing)
    $('#cap1').val(cap1)

    document.getElementById("form-id1").submit();

});



function requestData(){
    var requests = $.get('/data');
    // console.log(requests)

    var tm = requests.done(function(result){
      // console.log(result)
      $('#variable1').html(result[0])
      $('#variable2').html(result[1])
      $('#variable3').html(result[2])
    })
  }

  setInterval(function() {
    requestData();
  }, 100);