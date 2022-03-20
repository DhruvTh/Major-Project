var switchStatus = false;
$("#togBtn").on('change', function() {
    switchStatus = $(this).is(':checked');
        // alert(switchStatus);// To verify
    var cop = 'off'
    if(switchStatus == true){
        cop = 'on'
    }
    // alert(processing)
    $('#cop').val(cop)

    document.getElementById("form-id").submit();

});


var switchStatus1 = false;
$("#togBtn1").on('change', function() {
    switchStatus1 = $(this).is(':checked');
        // alert(switchStatus);// To verify
    var cap1 = '0'
    if(switchStatus1 == true){
        cap1 = '1'
    }
    // alert(processing)
    $('#cap1').val(cap1)

    document.getElementById("form-id1").submit();

});




function requestData(){
    var requests = $.get('/avp');
    // console.log(requests)

    var tm = requests.done(function(result){
      console.log(result)
      $('#variable1').html(result[0])
      $('#variable2').html(result[1])
      $('#variable3').html(result[2])
      $('#variable4').html(result[3])
      $('#variable5').html(result[4])
      $('#variable6').html(result[5])
      $('#variable7').html(result[6])


    })
  }

  setInterval(function() {
    requestData();
  }, 100);



  function requestData1(){
    var requests = $.get('/emsg');
    // console.log(requests)

    var tm = requests.done(function(result){
      // console.log(result[0])
      if(result[0] == '0'){
        $('#emsg').html('<div class="alert alert-warning" role="alert">Connection lost!!! <span onclick="makeConnection()" id="restart" class="alert-link">Reconnect Arduino</span>.</div>')
      }else{
        $('#emsg').html('');
      }
    })
  }

  setInterval(function() {
    requestData1();
  }, 2000);

function makeConnection(){
  $('#connection').val('1')
  console.log("sdffdgf")
  document.getElementById('formConnection').submit();
}

function updateTextInput(val) {
  document.getElementById('textInput').innerHTML =val; 
  document.getElementById("sliderForm").submit();
}
let value = $('#rangeInput').val()
$('#textInput').html(value) 


function updateTextInput1(val) {
  document.getElementById('textInput1').innerHTML =val; 
  document.getElementById("sliderForm1").submit();
}
let value1 = $('#rangeInput1').val()
$('#textInput1').html(value1) 


function updateTextInput2(val) {
  document.getElementById('textInput2').innerHTML =val; 
  document.getElementById("sliderForm2").submit();
}
let value2 = $('#rangeInput2').val()
$('#textInput2').html(value2)