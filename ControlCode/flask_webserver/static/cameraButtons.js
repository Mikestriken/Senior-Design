
{
    // * Create socket
    let socket = io.connect();
    // let socketTopic = "camera_state";
    
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
    /* socket.on('frame', function(data) {
        // let image = new Blob([data.image], {type: 'image/jpeg'});
        // let imageUrl = URL.createObjectURL(image);
        // cameraStream.src = imageUrl;

        // Convert ArrayBuffer to Uint8Array
        // let uint8Array = new Uint8Array(data.frame);

        // Convert Uint8Array to base64 string
        // let base64String = btoa(String.fromCharCode.apply(null, uint8Array));
        
        // cameraStream.src = "data:image/jpeg;base64," + data.frame;

        var blob = new Blob([data.frame], { type: 'image/jpeg' });
        var urlCreator = window.URL || window.webkitURL;
        var imageUrl = urlCreator.createObjectURL(blob);
        cameraStream.src = imageUrl;
    }); */

    function externalCameraButtonReleasedEventHandler() {
        window.location.href = "/outdoor_video_feed";
        /* popup.style.display = "flex";
        // socket.emit('switch_to_outdoor');
        
        // Update outdoor video feed
        updateInterval = setInterval(function() {
            updateImageSource(cameraStream, "/outdoor_video_feed");
        }, 0); // Update every second */
    }
    
    function internalCameraButtonReleasedEventHandler() {
        window.location.href = "/indoor_video_feed";
        /* popup.style.display = "flex";
        // socket.emit('switch_to_indoor');
        
        // Update indoor video feed
        updateInterval = setInterval(function() {
            updateImageSource(cameraStream, "/indoor_video_feed");
        }, 0); // Update every second */
    }
    
    function popupCloseButtonReleasedEventHandler() {
        popup.style.display = "none";
        // socket.emit('switch_to_none');
        
        clearInterval(updateInterval);

        // reload page
        location.reload();
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