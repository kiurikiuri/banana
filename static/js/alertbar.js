let AlertBar = class {
	constructor(id){
		this.alertbar = $(id);
	}
	show(){
		$(this.alertbar).show();
	}
	hide(){
		$(this.alertbar).hide();
	}
}

