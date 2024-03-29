import { fetchURL } from './modules.js';

{
    // * Create socket
    let socket = io.connect();
    let socketTopic = "door";
    
    // * JS Code for Buttons
    // * Get button objects and assign them to aliases
    const openButtonProgress = document.getElementById("openDoorProgress");
    const openButton = document.getElementById("openDoorButton");

    const closeButtonProgress = document.getElementById("closeDoorProgress");
    const closeButton = document.getElementById("closeDoorButton");

    const stopButton = document.getElementById("stopDoorButton");

    function setPressedStyle(button) {
        button.style.backgroundColor = 'hsl(228, 66%, 70%)';
    }

    function setReleasedStyle(button) {
        button.style.backgroundColor = 'hsl(228, 66%, 47%)';
    }

    function updateProgress(buttonProgress, progress){
        // * Define graphic update logic
        if (progress <= 100)
            buttonProgress.style.width = progress + '%';
    }

    // * Define what happens when the open button is pressed
    function openButtonPressedEventHandler(event) {
        setPressedStyle(openButton);
        setPressedStyle(openButtonProgress);
        document.addEventListener("mouseup", openButtonReleasedEventHandler);
        document.addEventListener("touchend", openButtonReleasedEventHandler);
    }

    // * Define what happens when the open button is released
    function openButtonReleasedEventHandler(event) {
        document.removeEventListener("mouseup", openButtonReleasedEventHandler);
        document.removeEventListener("touchend", openButtonReleasedEventHandler);
        
        if (!openButton.contains(event.target)) {
            setReleasedStyle(openButton);
            setReleasedStyle(openButtonProgress);
        } else {
            // setReleasedStyle(openButton);
            setReleasedStyle(closeButton);
            setReleasedStyle(openButtonProgress);
            
            // Asynchronously send open button event
            fetchURL('/openButton/click');

            // for (let i = 0; i <= 100; ++i)
            //     setTimeout(() => {updateProgress(openButtonProgress, i)}, i*100);
            
            // Create a new instance of updateProgress for openButton
            // const openButtonUpdateProgress = updateProgress(openButtonProgress);
            
            // let openInterval;
            // openInterval = setInterval(()=>{openButtonUpdateProgress(openInterval);}, 100);
        }
    }

    // * Define what happens when the close button is pressed
    function closeButtonPressedEventHandler() {
        setPressedStyle(closeButton);
        setPressedStyle(closeButtonProgress);
        document.addEventListener("mouseup", closeButtonReleasedEventHandler);
        document.addEventListener("touchend", closeButtonReleasedEventHandler);
    }

    // * Define what happens when the close button is released
    function closeButtonReleasedEventHandler(event) {
        document.removeEventListener("mouseup", closeButtonReleasedEventHandler);
        document.removeEventListener("touchend", closeButtonReleasedEventHandler);

        if (!closeButton.contains(event.target)) {
            setReleasedStyle(closeButton);
            setReleasedStyle(closeButtonProgress);
        }
        else {
            // setReleasedStyle(closeButton);
            setReleasedStyle(openButton);
            setReleasedStyle(closeButtonProgress);
            
            // Asynchronously send close button event
            fetchURL('/closeButton/click');

            //for (let i = 0; i <= 100; ++i)
            //    setTimeout(() => {updateProgress(closeButtonProgress, i)}, i*100);
            
            // Create a new instance of updateProgress for closeButton
            // const closeButtonUpdateProgress = updateProgress(closeButtonProgress);
            
            // let closeInterval;
            // closeInterval = setInterval(()=>{closeButtonUpdateProgress(closeInterval);}, 100);
        }
    }

    // * Define what happens when the stop button is pressed
    function stopButtonPressedEventHandler() {
        // Asynchronously send close button event
        fetchURL('/stopButton/click');
        stopButton.style.backgroundColor = 'hsl(0, 100%, 30%)';
    }

    // * Define what happens when the stop button is released
    function stopButtonReleasedEventHandler() {
        stopButton.style.backgroundColor = 'hsl(0, 100%, 50%)';
    }

    socket.on(socketTopic, function (msg) {
        // * Convert JSON text → JavaScript Object
        console.log(msg);
    
        updateProgress(openButtonProgress, msg);
        updateProgress(closeButtonProgress, 100 - msg);
    });

    // * Create an event listener (( Interrupt )) mouse or finger press and release
        // * On interrupt run relevant function.
    openButton.addEventListener("mousedown", openButtonPressedEventHandler);
    openButton.addEventListener("touchstart", openButtonPressedEventHandler);
    // openButton.addEventListener("mouseup", openButtonReleasedEventHandler);
    // openButton.addEventListener("touchend", openButtonReleasedEventHandler);

    closeButton.addEventListener("mousedown", closeButtonPressedEventHandler);
    closeButton.addEventListener("touchstart", closeButtonPressedEventHandler);
    // closeButton.addEventListener("mouseup", closeButtonReleasedEventHandler);
    // closeButton.addEventListener("touchend", closeButtonReleasedEventHandler);

    stopButton.addEventListener("mousedown", stopButtonPressedEventHandler);
    stopButton.addEventListener("touchstart", stopButtonPressedEventHandler);
    stopButton.addEventListener("mouseup", stopButtonReleasedEventHandler);
    stopButton.addEventListener("touchend", stopButtonReleasedEventHandler);

    function iterate() {
        let i = 0;
        function loop() {
            if (i <= 100) {
                updateBattery(i);
                i++;
                setTimeout(loop, 250);
            }
        }
        loop();
    }
    
    // Start iterating
    // iterate();
}