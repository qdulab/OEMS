$(document).ready(function (){
    create_lesson_category()
})

function create_lesson_category(){
    $("button").click(function (){
        $.post('/teacher/category/create/',
               {name:$('#lesson_category_name').val()},
               function (data){
                   alert("创建成功"+data.id)
                   $("tbody").prepend("<tr><td><a href='/teacher/lesson_list/"+data.id+"/'>"+$('#lesson_category_name').val()+"</a></td><td>0</td><td></td></tr>")
               })
        return false;
    })
}
