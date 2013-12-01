$(document).ready(function (){
    create_lesson_category();
})

function create_lesson_category(){
    $("button").click(function (){
        $.post('/teacher/category/create/',
               {name:$('#lesson_category_name').val()},
               function (data){
                   var response = eval('(' + data + ')');
                   if (response.status == 1){
                        var str = "<tr><td><a href='/teacher/lesson_list/"+response.id+"/'>"+$('#lesson_category_name').val()+"</a></td><td>0</td><td>"+response.date.y+"年"+response.date.m+"月"+response.date.d+"日 "+response.time+"</td></tr>";
                        $("tbody").prepend(str);
                        //TODO 页面缓存
                        alert("创建成功！");
                    }
                    else if(response.status == 0){
                        alert("科目已经存在！");
                    }
               })
        return false;
    })
}
