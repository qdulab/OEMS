$(document).ready(function (){
    modify_profile();
})

function modify_profile(){
    $("#modify_profile").click(function (){
        form = $("teacher_profile");

        $.ajax({
            address: form.attr('address'),
            mobile: form.attr('mobile'),
            QQ: form.attr('QQ'),
            blog: form.attr('blog'),
            data: frm.serialize(),
            success: function (data) {
                var response = JSON.parse(data);
                if(response.status == 1)
                    Messenger().post("修改成功！")
            },
        })
        return false;
    })
}


