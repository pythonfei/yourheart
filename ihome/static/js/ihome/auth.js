function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}
$(document).ready(function(){
	$("#real-name").focus(function(){
        $("#error-msg").hide();});
  $("#id_card").focus(function(){
        $("#error-msg").hide(); });    
	$.get("/api/auth",function(data){
		if("0" == data.errno){
			$("#real-name").val(data.data.real_name);
			$("#real-name").prop({display:true});
			$("#id-card").val(data.data.id_card);
			$("#id-card").prop({display:true});
			$("#submit").hide();
		}
	});
	
	$("#form-auth").submit(function(e){
		e.preventDefault();
		var options ={
				url:"/api/auth",
				type:"post",
	      headers:{
	          "X-XSRFTOKEN":getCookie("_xsrf"),
	      },
			
				success:function(data){
					if ("0" != data.errno){
						alert(data.errmsg)
						$("#error-msg").show()
					}else{
						window.location.href="my.html"
					}
				}
			};
		$(this).ajaxSubmit(options);
		})
})

