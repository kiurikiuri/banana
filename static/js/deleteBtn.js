let DeleteBtn = class {
	constructor(className){
		this.deleteBtn = $(className);
    this.status = 0;
    this.hide();
	}
	show(){
		$(this.deleteBtn).show();
    this.status = 1;
	}
	hide(){
		$(this.deleteBtn).hide();
    this.status = 0;
	}
  getKey(){
    let arr =[];
    $(this.deleteBtn).each(function(index, element){
      let el = $(element).find("input[type='checkbox']");
      if ( $(el).prop("checked") == 1 ){
        arr.push($(el).attr('data-id'));
      }
    });
    return arr;
  }
}

let btn = new DeleteBtn(".delete-btns");

let delete_trg_btn = $('#delete_trg_btn');
let cansel = $('#cansel');

function getObjArr(arr, deli){
  items = []
  arr.forEach(function(el){
    rec = el.split(deli);
    items.push({id: rec[0],kind_id: rec[1]});
  });
  return items;
}



$(delete_trg_btn).on('click', function(){
  console.log(1)
  if (btn.status == 0){
    $(delete_trg_btn).text('ONE MORE PUSH');
    $(cansel).show();
    btn.show();
  }else{
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
    $("#deleteItems").val(str);
    $("#form").submit();
  }
})

