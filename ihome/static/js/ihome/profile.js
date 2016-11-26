// function showSuccessMsg() {
//     $('.popup_con').fadeIn('fast', function() {
//         setTimeout(function(){
//             $('.popup_con').fadeOut('fast',function(){}); 
//         },1000) 
//     });
// }

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
		$.get("/api/profile/avatar",function(data){
			if ("0" == data.errno){
				$("#user-avatar").attr("src", data.url);
			}
			
		})
    //上传头像
    $("#form-avatar").submit(function(e){
        e.preventDefault();

        $('.image_uploading').fadeIn('fast');
        alert($('.image_uploading').attr("class"))
        var options = {
            url:"/api/profile/avatar",
            type:"POST",
            headers:{
                "X-XSRFTOKEN":getCookie("_xsrf"),
            },
            success: function(data){

                if ("0" == data.errno) {
                		// $('.image_uploading').fadeIn('fast');
                    $(".image_uploading").fadeOut('fast');
                    $("#user-avatar").attr("src", data.url);
                }else{
                	alert(data.errmsg)
                }
            }
        };
        $(this).ajaxSubmit(options);
    });
})