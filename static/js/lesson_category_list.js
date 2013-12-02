$(document).ready(function (){
    create_lesson_category();
})

function create_lesson_category(){
    $("#create_button").click(function (){
        var input_name = $('#lesson_category_name').val();
        if(input_name.length <= 60 && input_name.length > 0){
            $.post('/teacher/category/create/',
               {name: input_name,
                csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]').val()},
               function (data){
                   var response = JSON.parse(data);
                   if (response.status == 1){
                        var str = "<tr><td><a href='/teacher/lesson_list/"+response.id+"/'>"+input_name+"</a></td><td>0</td><td>"+response.date.y+"年"+response.date.m+"月"+response.date.d+"日 "+response.time+"</td></tr>";
                        $("tbody").prepend(str);
                        alert("创建成功！");
                    }
                    else if(response.status == 0){
                        alert("科目已经存在！");
                    }
               })
        }
        else if(input_name.length > 60)
            alert("科目名长度超过60个字符！请重新输入！");       
        else 
            alert("请输入科目名称！");
        $('#lesson_category_name').val("");
        return false;
    })
}
