{
    // * Create object on html subdirectory to register events on
    // const eventSource = new EventSource('/alert-events');

    const messageBoxScroller = document.getElementById('messagesTextbox');
    const messageBox = document.getElementById('messageBoxContent');
    const clearButton = document.getElementById('clearTextboxButton');

    // eventSource.onmessage = function(event) {
    //     // * Convert JSON text → JavaScript Object
    //     console.log(event);
    //     const jsonData = JSON.parse(event.data);

    //     messageBox.innerHTML += `\n<span>${jsonData.alert}</span>`;

    //     messageBoxScroller.scrollTop = messageBoxScroller.scrollHeight;
    // }
    
    function clearMessages() {
        while(messageBox.firstChild){
            messageBox.removeChild(messageBox.firstChild);
        }
    }

    clearButton.addEventListener("mouseup", clearMessages)
    clearButton.addEventListener("touchend", clearMessages)
    
    var socket = io.connect();
    
    socket.on("alert", function (msg) {
        // * Convert JSON text → JavaScript Object
        console.log(msg);
    
        messageBox.innerHTML += `\n<span>${msg}</span>`;
    
        messageBoxScroller.scrollTop = messageBoxScroller.scrollHeight;
      });
}