

$(function(){


$.ajax({
    url:"/app/get_all_subjects",
    success:function(data){
        console.log(data);
        grades=data;

        for(i=0;i<grades.length;i++)
        {
           $("#class-sel").append('<option value="'+grades[i]['id']+'">'+grades[i]['grade']+'</option>')
        }
        for(i=0;i<grades[0]['subjects'].length;i++)
        {
           $("#subject-sel").append('<option value="'+grades[0]['subjects'][i]["id"]+'">'+grades[0]['subjects'][i]["name"]+'</option>')
        }

    }

})


$("#class-sel").change(function(){
    var grade = grades.filter(function( obj ) {
        return obj['grade'] == $("#class-sel").val();
    })[0];
    console.log(grade);
    $("#subject-sel").html('');
    for(i=0;i<grade['subjects'].length;i++)
    {
        $("#subject-sel").append('<option value="'+grade['subjects'][i]["id"]+'">'+grade['subjects'][i]["name"]+'</option>')
    }

})
})