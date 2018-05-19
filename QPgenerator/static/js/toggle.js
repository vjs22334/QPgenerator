
var $ = django.jQuery


$(document).ready(function(){
    function toggleInline(selected){
        $("#choice_set-group").hide();
        $("#match_set-group").hide();
        if(selected === "mcq")
            $("#choice_set-group").show();
        else if(selected === "Match")
            $("#match_set-group").show();
    }
    
    
    var $q_type = $("#id_question_type");
    toggleInline($q_type.val());
    $q_type.change(function(){
        toggleInline($q_type.val())
        console.log($q_type.val())
    });
});