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


let isUrl = $('#correct-answer').text()
AutoLink(isUrl);
function AutoLink(str) {
    var regexp_url = /((h?)(ttps?:\/\/[a-zA-Z0-9.\-_@:/~?%&;=+#',()*!]+))/g; // ']))/;
    var regexp_makeLink = function(all, url, h, href) {
        return '<a href="h' + href + '">' + url + '</a>';
    }
 
    return str.replace(regexp_url, regexp_makeLink);
}


