
{
    // * Create socket
    let socket = io.connect();
    let socketTopic = "camera_state";
    
    // * JS Code for Buttons
    // * Get button objects and assign them to aliases
    const externalCameraButton = document.getElementById("externalCameraButton");
    const internalCameraButton = document.getElementById("internalCameraButton");
    const popupCloseButton = document.getElementById("popupCloseButton");
    const popup = document.getElementById("popup");
    const cameraStream = document.getElementById("cameraStream");
    
    // * Locally Global Variable
    let updateInterval;
    
    // Function to update the image source with the new frame
    function updateImageSource(imgElement, endpoint) {
        imgElement.src = endpoint + "?" + new Date().getTime(); // Append a timestamp to force image reload
    }

    function externalCameraButtonReleasedEventHandler() {
        popup.style.display = "flex";

        // Update outdoor video feed
        updateInterval = setInterval(function() {
            updateImageSource(cameraStream, "/outdoor_video_feed");
        }, 1000); // Update every second
    }
    
    function internalCameraButtonReleasedEventHandler() {
        popup.style.display = "flex";
        
        // Update indoor video feed
        updateInterval = setInterval(function() {
            updateImageSource(cameraStream, "/indoor_video_feed");
        }, 1000); // Update every second
    }
    
    function popupCloseButtonReleasedEventHandler() {
        popup.style.display = "none";
        
        clearInterval(updateInterval);
    }

    
    // * Create an event listener (( Interrupt )) mouse or finger press and release
        // * On interrupt run relevant function.
    // externalCameraButton.addEventListener("mousedown", externalCameraButtonPressedEventHandler);
    // externalCameraButton.addEventListener("touchstart", externalCameraButtonPressedEventHandler);
    externalCameraButton.addEventListener("mouseup", externalCameraButtonReleasedEventHandler);
    externalCameraButton.addEventListener("touchend", externalCameraButtonReleasedEventHandler);
    
    // internalCameraButton.addEventListener("mousedown", internalCameraButtonPressedEventHandler);
    // internalCameraButton.addEventListener("touchstart", internalCameraButtonPressedEventHandler);
    internalCameraButton.addEventListener("mouseup", internalCameraButtonReleasedEventHandler);
    internalCameraButton.addEventListener("touchend", internalCameraButtonReleasedEventHandler);

    // popupCloseButton.addEventListener("mousedown", popupCloseButtonPressedEventHandler);
    // popupCloseButton.addEventListener("touchstart", popupCloseButtonPressedEventHandler);
    popupCloseButton.addEventListener("mouseup", popupCloseButtonReleasedEventHandler);
    popupCloseButton.addEventListener("touchend", popupCloseButtonReleasedEventHandler);

    // popup.addEventListener("mousedown", popupPressedEventHandler);
    // popup.addEventListener("touchstart", popupPressedEventHandler);
    popup.addEventListener("mouseup", popupCloseButtonReleasedEventHandler);
    popup.addEventListener("touchend", popupCloseButtonReleasedEventHandler);
}