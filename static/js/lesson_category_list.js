$(document).ready(function (){
    $("button").click(function (){
        alert("he")
        $.post('/teacher/category/create/',
               {name:$('#lesson_category_name').val()},
               function (){
                   alert("创建成功")
               })
        alert("hehe")
        return false;
    })
})
