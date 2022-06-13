$('#btn-answer').on('click', function(){
  console.log(1)
  $('.after-answer').removeClass('d-none');
  $('.after-answer').addClass('d-block');
  $(this).hide();
  
})
$("#correct-btn").on('click', function(){
  //$("#addItems").val(str);
  $("#actionflg").val("correct");
  $("#form").submit();
})
$("#incorrect-btn").on('click', function(){
  //$("#addItems").val(str);
  $("#actionflg").val("incorrect");
  $("#form").submit();
})


