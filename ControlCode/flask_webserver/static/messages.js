{
    const messageBox = document.getElementById('messagesTextbox');
    const clearButton = document.getElementById('clearTextboxButton');

    let i = 5;
    function addMessage () {
        messageBox.innerHTML += `\n<span>text${i}</span>`
        ++i;
    }

    setInterval(addMessage, 3000);
}