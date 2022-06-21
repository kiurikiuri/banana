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


$(function(){
    $('.js-autolink').each(function(){
        $(this).html($(this).html().replace(/(\b(https?|ftp|file):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/ig,"<a href='$1'>$1</a>"));
    });
});
