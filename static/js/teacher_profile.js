$(document).ready(function (){
    modify_profile();
})

function modify_profile(){
    $("#modify_profile").click(function (){
        form = $("form#teacher_profile");

        $.ajax({
            type: form.attr('method'),
            url: form.attr('action'),
            data: form.serialize(),
            success: function (data) {
                var response = JSON.parse(data);
                if(response.status == "ok")
                    Messenger().post("修改成功！");
                else if(response.status == "fail")
                    Messenger().post({
                        message: "修改失败！",
                        type: "error"
                    })
            },
        });
        return false;
    })
}


