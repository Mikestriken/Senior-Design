// * JS Code for Buttons
// * Get button objects and assign them to aliases
const openButton = document.getElementById("openDoorButton");
const closeButton = document.getElementById("closeDoorButton");

// * Define what happens when the open button is pressed
function openButtonEventHandler() {
    window.location.href = "/index.html";
}

// * Define what happens when the close button is pressed
function closeButtonEventHandler() {
    window.location.href = "/index.html";
}

// * Create an event listener (( Interrupt )) for when openButton or closeButton is "clicked".
// * On interrupt run relevant function.
openButton.addEventListener("click", openButtonEventHandler);
closeButton.addEventListener("click", closeButtonEventHandler);