$(function(){

    eel.expose(say_hello_js);               // Expose this function to Python
    function say_hello_js(x) {
        let txtArea = document.getElementById('textArea');
        txtArea.value = x.toString();
    }
    
    //say_hello_js("Javascript World!");
    //eel.handleinput("connected!");  // Call a Python function
    
    $("#btn").click(function(){
        eel.handleinput($("#inp").val());
        $('#inp').val('');
    });
}); 