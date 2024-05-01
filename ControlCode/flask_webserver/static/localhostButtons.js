import { fetchURL } from './modules.js';
{
    // * Create socket
    let socket = io.connect();
    const ipSocketTopic = "host_ip";
    const currentSensorStatusSocketTopic = "current_sensor";

    const terminalButton = document.getElementById("terminalButton");
    const rebootButton = document.getElementById("rebootButton");

    function getIP() {
        return new Promise((resolve, reject) => {
            socket.on(ipSocketTopic, function (msg) { resolve(msg.data) });
        });
    }

    function getCurrentStatus() {
        return new Promise((resolve, reject) => {
            socket.on(currentSensorStatusSocketTopic, function (msg) { resolve(msg.data) });
        });
    }
    
    async function terminalButtonReleasedEventHandler() {
        // Request and retrieve the IPv4 Address of webserver on local network.
        socket.emit(ipSocketTopic);
        let host_ip = getIP();
        let currentSensorStatus = getCurrentStatus();

        // Display an alert textbox with relevant information.
        window.alert(`To Open a Terminal Press: Ctrl + Alt + T\nAlternatively the IPv4 Address webserver to ssh into is: ${await host_ip}\nCurrent Sensor: ${await currentSensorStatus}`);
    }

    function rebootButtonReleasedEventHandler() {
        fetchURL('/localhost/reboot');
    }


    terminalButton.addEventListener("mouseup", terminalButtonReleasedEventHandler);
    terminalButton.addEventListener("touchend", terminalButtonReleasedEventHandler);

    rebootButton.addEventListener("mouseup", rebootButtonReleasedEventHandler);
    rebootButton.addEventListener("touchend", rebootButtonReleasedEventHandler);
}