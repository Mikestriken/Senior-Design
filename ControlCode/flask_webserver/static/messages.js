{
    // * Create socket
    let socket = io.connect();
    let socketTopic = "alert";

    const messageBoxScroller = document.getElementById('messagesTextbox');
    const messageBox = document.getElementById('messageBoxContent');
    const clearButton = document.getElementById('clearTextboxButton');
    
    socket.on(socketTopic, function (msg) {
        // * Convert JSON text → JavaScript Object
        // console.log(msg);
    
        messageBox.innerHTML += `\n<span>${msg}</span>`;
    
        messageBoxScroller.scrollTop = messageBoxScroller.scrollHeight;
      });
    
    function clearMessages() {
        while(messageBox.firstChild){
            messageBox.removeChild(messageBox.firstChild);
        }
    }

    clearButton.addEventListener("mouseup", clearMessages)
    clearButton.addEventListener("touchend", clearMessages)
    
}