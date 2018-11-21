import $ from jquery;

// function clearField() {
//     document.getElementById("chatField").value = ""
// }

$(document).ready(function() {
    $("#clearButton").click(function() {
        alert("it works");
        document.getElementById("chatField").value = "";
    });
    
    $("#submitButton").click(function() {
        var chatData = document.getElementById("chatField").value;
        
        // $.ajax({
        //     url: "http://localhost:8080",
        //     type: "POST",
        //     data: chatData,
        //     dataType: "jsonp",
        //     jsonpCallback: function() {
        //         console.log("jsonp success");
        //     },
        //     success: function (data) {
        //         alert("Success!");
        //     },
        // });
        
        $.post("http://localhost:8080", chatData, () => {
            alert("Success!");
        })
    });
    
});
