$(document).ready(function(){
    update_student_profile();
})
function update_student_profile(){
    $("button#update_student_profile").click(function(){
        var school_id = $("input#school_id").val();
        form = $("form#student_profile");
        alert(form.attr("method"));
        if(school_id.length <= 20 && school_id.length > 0){
            $.ajax({
                type: form.attr("method"),
                url: form.attr("action"),
                dataType: "json",
                data: form.serialize(),
                error: function(){
                    alert("fail");
                },
                success:function(data){
                    alert("succeed");
                    var response = JSON.parse(data);
                    if(response.status == 1){
                        $("input#school_id").text(response.school_id);
                        Messager().post("更新成功")
                    }
                    else if(response.status == "fail"){
                        Messager().post({
                            message: "失败",
                            type: "error"
                        })
                    }
                }
            })
        }
    })
}
