import { fetchURL } from './modules.js';
{
    const terminalButton = document.getElementById("terminalButton");
    const rebootButton = document.getElementById("rebootButton");

    function terminalButtonReleasedEventHandler() {
        window.alert('To Open a Terminal Press: Ctrl + Alt + T');
    }

    function rebootButtonReleasedEventHandler() {
        fetchURL('/localhost/reboot');
    }


    terminalButton.addEventListener("mouseup", terminalButtonReleasedEventHandler);
    terminalButton.addEventListener("touchend", terminalButtonReleasedEventHandler);

    rebootButton.addEventListener("mouseup", rebootButtonReleasedEventHandler);
    rebootButton.addEventListener("touchend", rebootButtonReleasedEventHandler);
}