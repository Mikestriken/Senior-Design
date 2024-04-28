import { fetchURL } from './modules.js';
{
    // * Create socket
    let socket = io.connect();
    let socketTopic = "host_ip";

    const terminalButton = document.getElementById("terminalButton");
    const rebootButton = document.getElementById("rebootButton");

    function getIP() {
        return new Promise((resolve, reject) => {
            socket.on(socketTopic, function (msg) { resolve(msg.data) });
        });
    }
    
    async function terminalButtonReleasedEventHandler() {
        // Request and retrieve the IPv4 Address of webserver on local network.
        socket.emit(socketTopic);
        let host_ip = await getIP();

        // Display an alert textbox with relevant information.
        window.alert(`To Open a Terminal Press: Ctrl + Alt + T\nAlternatively the IPv4 Address webserver to ssh into is: ${host_ip}`);
    }

    function rebootButtonReleasedEventHandler() {
        fetchURL('/localhost/reboot');
    }


    terminalButton.addEventListener("mouseup", terminalButtonReleasedEventHandler);
    terminalButton.addEventListener("touchend", terminalButtonReleasedEventHandler);

    rebootButton.addEventListener("mouseup", rebootButtonReleasedEventHandler);
    rebootButton.addEventListener("touchend", rebootButtonReleasedEventHandler);
}