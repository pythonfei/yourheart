function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
		$.get("/api/profile/avatar",function(data){
			if ("0" == data.errno){
				$("#user-avatar").attr("src", data.url);
			}else{
                window.location.href="login.html"
            }
			
		})
        //加载名字
        $.get("/api/profile/name",function(data){
            if("0" == data.errno){
                $("#user-name").val(data.data);
            }else{
                alert(data.errmsg)
            }
        })
    //上传头像
    $("#form-avatar").submit(function(e){
        e.preventDefault();

        $('.image_uploading').fadeIn('fast');
        var options = {
            url:"/api/profile/avatar",
            type:"POST",
            headers:{
                "X-XSRFTOKEN":getCookie("_xsrf"),
            },
            success: function(data){

                if ("0" == data.errno) {
                    showSuccessMsg() 
                    $(".image_uploading").fadeOut('fast');
                    $("#user-avatar").attr("src", data.url);
                }else{
                    $(".popup p").text(data.errmsg);
                    showSuccessMsg() ;
                    $(".image_uploading").fadeOut('fast');

                }
            }
        };
        $(this).ajaxSubmit(options);
    });
    $("#form-name").submit(function(e){
        e.preventDefault();
        $("#user-name").focus(function(){
            $(".error-msg").hide()
        })
        $('.image_uploading').fadeIn('fast');
        var name_data = {name_data:$("#user-name").val()};
        console.log(name_data)
        $.ajax({
            url:"/api/profile/name",
            type:"post",
            data:JSON.stringify(name_data),
            contentType:"application/json",
            dataType:"json",
            headers:{
                "X-XSRFTOKEN":getCookie("_xsrf"),
            },
            success:function(data){
                if("0" == data.errno){
                    showSuccessMsg() 
                    $(".image_uploading").fadeOut('fast');
                    $("#user-name").val(data.name);

                }else{
                    $(".popup p").text(data.errmsg);
                    showSuccessMsg() ;
                    $(".image_uploading").fadeOut('fast');
                    $(".error-msg").text(data.errmsg);
                    $(".error-msg").show();
                }
            }
        })
    })
})