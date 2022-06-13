let fileInput = document.getElementById('csv_file');
let submitbtn = document.getElementById('submit');
let message = document.getElementById('message');
let fileReader = new FileReader();
let addtype = '';

// ファイル変更時イベント
submitbtn.onclick = () => {
  addtype = $(submitbtn).data('addtype');
  console.log(addtype);
  let file = fileInput.files[0];
  fileReader.readAsText(file, "Shift_JIS");
};

// ファイル読み込み時
var items = [];
fileReader.onload = () => {
  // ファイル読み込み
  var fileResult = fileReader.result.split('\r\n');

  // 先頭行をヘッダとして格納
  let header = fileResult[0].split(',');
  // 先頭行の削除
  fileResult.shift();
  fileResult.pop();


  // CSVから情報を取得
  items = fileResult.map(item => {
    let datas = item.split(',');
    let result = {};
    for (const index in datas) {
      let key = header[index];
      result[key] = datas[index];
    }
    return result;
  });

//let jsondata = JSON.stringify(fileResult);

if ($('#my_form').hasClass('new_deck_form')){
  console.log(items);
  items.push({'deck_name' : $('#deck_name').val() });
  console.log(items);
}

let jsondata = JSON.stringify(items);
console.log(jsondata);
    $.ajax({
        url: '/readcsv/'+addtype,
        type: 'post',
        data: jsondata,
        dataType: "json"
    }).done(function(data){
    	console.log(data);
    	let rtn = JSON.parse(data.values);
      let alertclass = "alertbar-" + Math.random().toString(32).substring(2);
      let newalert = $(".alertbar_tmp").clone(true).removeClass('alertbar_tmp').addClass(alertclass);
      $(newalert).appendTo($("body"));
      $(newalert).find("strong").text(rtn.title);
      $(newalert).find("p").text(rtn.message);
      $(newalert).show();
    }).fail(function(data){
      console.log(data);
      let alertclass = "alertbar-" + Math.random().toString(32).substring(2);
      let newalert = $(".alertbar_tmp").clone(true).removeClass('alertbar_tmp alert-success').addClass(alertclass + ' alert-danger');
      $(newalert).appendTo($("body"));
      $(newalert).find("strong").text(data.statusText);
      $(newalert).find("p").text("failed");
      $(newalert).show();
    });
  


  return;
}
// ファイル読み取り失敗時
fileReader.onerror = () => {
  items = [];
  message.innerHTML = "ファイル読み取りに失敗しました。"
}

