// * JS Code for Buttons
// * Get button objects and assign them to aliases
const openButton = document.getElementById("openDoorButton");
const closeButton = document.getElementById("closeDoorButton");

// * Define what happens when the open button is pressed
function openButtonEventHandler() {

    // * Load this webpage subdirectory asynchronously so that we don't reload the page.
    fetch('/openButton/click')
    .then(response => {
        // Retrieve the HTTP status code of the response
        console.log('HTTP status code:', response.status);
    })
    .catch(error => {
        // Handle any errors that occurred during the fetch operation
        console.error('Error:', error);
    });
}

// * Define what happens when the close button is pressed
function closeButtonEventHandler() {

    // * Load this webpage subdirectory asynchronously so that we don't reload the page.
    fetch('/closeButton/click')
    .then(response => {
        // Retrieve the HTTP status code of the response
        console.log('HTTP status code:', response.status);
    })
    .catch(error => {
        // Handle any errors that occurred during the fetch operation
        console.error('Error:', error);
    });
}

// * Create an event listener (( Interrupt )) for when openButton or closeButton is "clicked".
// * On interrupt run relevant function.
openButton.addEventListener("click", openButtonEventHandler);
closeButton.addEventListener("click", closeButtonEventHandler);