$(document).ready(function(){
    create_experiment();
})

function create_experiment(){
    $().click(function(){
        var experiment_name = $("input#experiment_name").val();
        var experiment_content = $("input#experiment_content").val();
        var experiment_deadline = $("input#experiment_deadline").val();
        var experiment_information = $("input#experiment_information").val();
        var experiment_weight = $("input#experiment_weight").val();

        var form = $("form#create_experiment_form")

        $.ajax({
            type: form.attr("method"),
            url: form.attr("action"),
            data: form.serialize(),
            success: function(data){
                var response = JSON.parse(data);
                
                if(response.status_phrase == "ok"){
                    Messenger().post({
                        id: "create_experiment",
                        type: "success",
                        message: "创建成功"
                    })
                }
            }
        })
    return false;
    })
}
