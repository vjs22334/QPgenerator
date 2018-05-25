$("#id_grade").change(function () {
    var url = $("#personForm").attr("load-sub-url");  
    var gradeId = $(this).val();  

    $.ajax({                       
        url: '/app/load_subjects',                 
        data: {
        'grade': gradeId       
        },
        success: function (data) {   
        $("#id_subject").html(data); 
        }
    });
    })
    $("#id_subject").change(function () {
    var url = $("#personForm").attr("load-sub-url");  
    var subjectId = $(this).val();
    var gradeId = $("#id_grade").val();  

    $.ajax({                       
        url: '/app/load_chapters',                 
        data: {
        'grade': gradeId,
        'subject': subjectId       
        },
        success: function (data) {   
        $("#id_chapter").html(data); 
        }
    });

    });
