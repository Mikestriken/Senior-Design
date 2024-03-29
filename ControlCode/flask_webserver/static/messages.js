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

    // for (let i = 0; i <= 100; ++i)
    //     setTimeout(() => {
    //         messageBox.innerHTML += `\n<span>Alert Message ${i}</span>`;
        
    //         messageBoxScroller.scrollTop = messageBoxScroller.scrollHeight;
    //     }, i*1000);
    
}