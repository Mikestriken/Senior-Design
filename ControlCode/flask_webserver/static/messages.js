{
    const messageBoxScroller = document.getElementById('messagesTextbox');
    const messageBox = document.getElementById('messageBoxContent');
    const clearButton = document.getElementById('clearTextboxButton');

    let i = 5;
    function addMessage () {
        // let currentHTML = messageBox.innerHTML;
        messageBox.innerHTML += `\n<span>text${i}</span>`; // + currentHTML;
        ++i;

        messageBoxScroller.scrollTop = messageBoxScroller.scrollHeight;
    }

    setInterval(addMessage, 3000);

    function clearMessages() {
        while(messageBox.firstChild){
            messageBox.removeChild(messageBox.firstChild);
        }
    }

    clearButton.addEventListener("mouseup", clearMessages)
    clearButton.addEventListener("touchend", clearMessages)
}