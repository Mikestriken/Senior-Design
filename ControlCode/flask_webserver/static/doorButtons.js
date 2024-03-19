import { fetchURL } from './modules.js';

{
    // * JS Code for Buttons
    // * Get button objects and assign them to aliases
    const openButtonProgress = document.getElementById("openDoorProgress");
    const openButton = document.getElementById("openDoorButton");

    const closeButtonProgress = document.getElementById("closeDoorProgress");
    const closeButton = document.getElementById("closeDoorButton");

    const stopButton = document.getElementById("stopDoorButton");

    // // * Basic Fetch Function
    // async function fetchURL(url) {
    //     try {
    //         // * Load this webpage subdirectory asynchronously so that we don't reload the page.
    //         const response = await fetch(url)

    //         // * Log the Response
    //         console.log('HTTP status code:', response.status);
    //     }
    //     catch(error) {
    //         // * Handle any errors that occurred during the fetch operation
    //         console.error('Error:', error);
    //     }
    // }

    function setPressedStyle(button) {
        button.style.backgroundColor = 'hsl(228, 66%, 70%)';
    }

    function setReleasedStyle(button) {
        button.style.backgroundColor = 'hsl(228, 66%, 47%)';
    }

    function updateProgress(button){
        // * Define iterator variable
        let i = 0;
        
        // * Define graphic update logic
        return function (interval){
            if (i <= 100) {
                button.style.width = i + '%';
                i++;
            } else {
                clearInterval(interval)
                i=0;
            }
        }
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
            setReleasedStyle(openButtonProgress);
            
            // Asynchronously send open button event
            fetchURL('/openButton/click');
            
            // Create a new instance of updateProgress for openButton
            const openButtonUpdateProgress = updateProgress(openButtonProgress);
            
            let openInterval;
            openInterval = setInterval(()=>{openButtonUpdateProgress(openInterval);}, 100);
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
            setReleasedStyle(closeButtonProgress);
            
            // Asynchronously send close button event
            fetchURL('/closeButton/click')
            
            // Create a new instance of updateProgress for closeButton
            const closeButtonUpdateProgress = updateProgress(closeButtonProgress);
            
            let closeInterval;
            closeInterval = setInterval(()=>{closeButtonUpdateProgress(closeInterval);}, 100);
        }
    }

    // * Define what happens when the stop button is pressed
    function stopButtonPressedEventHandler() {
        // Asynchronously send close button event
        fetchURL('/closeButton/click')
        stopButton.style.backgroundColor = 'hsl(0, 100%, 30%)';
    }

    // * Define what happens when the stop button is released
    function stopButtonReleasedEventHandler() {
        stopButton.style.backgroundColor = 'hsl(0, 100%, 50%)';
    }

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
}