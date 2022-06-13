let SubmitBtn = class {
	constructor(className){
		this.chkBtn = $(className);
    this.status = 0;
    this.hide();
	}
	show(){
		$(this.chkBtn).show();
    this.status = 1;
	}
	hide(){
		$(this.chkBtn).hide();
    this.status = 0;
	}
  getKey(){
    let arr =[];
    $(this.chkBtn).each(function(index, element){
      let el = $(element).find("input[type='checkbox']");
      if ( $(el).prop("checked") == 1 ){
        arr.push($(el).attr('data-id'));
      }
    });
    return arr;
  }
}

let btn = new SubmitBtn(".add-btns");

let submit_btn = $('#submit');
let cansel = $('#cansel');

function getObjArr(arr, deli){
  items = []
  arr.forEach(function(el){
    rec = el.split(deli);
    items.push({id: rec[0],kind_id: rec[1]});
  });
  return items;
}



$(submit_btn).on('click', function(){
  console.log(1)
  if (btn.status == 0){
    $(submit_btn).text('ONE MORE PUSH');
    $(cansel).show();
    btn.show();
  }else{
    //arr = btn.getKey();
    arr = btn.getKey();
    str="";
    arr.forEach(function(el){
      if (str.length == 0){
        str = el;
      }else{
        str = str + "," + el;
      }
    });
    console.log(str);
    $("#addItems").val(str);
    $("#actionflg").val("add");
    $("#create_deck_form").submit();
  }
})


