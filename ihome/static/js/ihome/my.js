function logout() {
    $.get("/api/logout", function(data){
        if ("0" == data.errno) {
            location.href = "/";
        }else{
        	alert(data.errmsg)
        }
    })
}

$(document).ready(function(){
	$.get("/api/mymsg",function(data){
		if ("0" == data.errno ){
				$("#user-avatar").attr("src",data.data.img_url);
				$("#user-name").text(data.data.name);
				$("#user-mobile").text(data.data.mobile);
		}else{
			alert(data.errmsg);
			window.location.href='index.html'
		}
	})
})