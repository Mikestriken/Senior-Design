{
    // * Create socket
    let socket = io.connect();
    let socketTopic = "battery_state";

    // * Battery Test Animation
    // * Get HTML element objects for the % text and the graphic of battery.
    const batteryPercentage = document.getElementById("batteryPercentageOutput");
    const battery = document.getElementById("batteryGraphicOutput");

    // * Define graphic update logic
    function updateBattery(capacity) {
        if (capacity <= 100) {
            // * Size and Text
            battery.style.width = capacity + '%';
            batteryPercentage.innerHTML = '⚡' + Math.round(capacity) + '%';

            // * Color
            if (capacity === 100) {
                battery.style.backgroundColor = "lime";
            } else {
                // Change color as percentage increases
                const redValue = Math.floor((200 - 2*capacity) * 255 / 100);
                const greenValue = Math.floor(2 * capacity * 255 / 100);
                battery.style.backgroundColor = `rgb(${redValue}, ${greenValue}, 0)`;
            }
        }
    }

    socket.on(socketTopic, function (msg) {
        // * Convert JSON text → JavaScript Object
        // console.log(msg);
    
        updateBattery(msg);
    });

    function iterate() {
        let i = 0;
        function loop() {
            if (i <= 100) {
                updateBattery(i);
                i++;
                setTimeout(loop, 250);
            }
            else {
                i = 0;
                setTimeout(loop, 250);
            }
        }
        loop();
    }
    
    // Start iterating
    iterate();
}