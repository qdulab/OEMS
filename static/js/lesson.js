$(document).ready(function(){
    create_lesson();
})

function create_lesson(){
    $("button#submit_lesson_info").click(function(){
        var category = $("select#category").val();
        var name = $("input#lesson_name").val();
        var info = $("textarea#lesson_info").val();

        form = $("form#create_lesson_form");

        $.ajax({
            type: form.attr("method"),
            url: form.attr("action"),
            data: form.serialize(),
            success: function(data){
                var response = JSON.parse(data);
                if(response.status_phrase == "ok"){
                    Messenger().post({
                        id: "create_lesson",
                        type: "success",
                        message: "创建成功"
                    })
                    $("form#create_lesson_form").load("./ #create_lesson_form");
                }
                else if(response.status_phrase == "fail"){
                    Messenger().post({
                        id: "create_lesson",
                        type: "error",
                        message: "创建失败"
                    })
                }
            }
        })
    return false;
    })
}
