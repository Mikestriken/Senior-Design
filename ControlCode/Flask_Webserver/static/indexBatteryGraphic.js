// * Battery Test Animation
// * Get HTML element objects for the % text and the graphic of battery.
const batteryPercentage = document.getElementById("batteryPercentageOutput");
const battery = document.getElementById("batteryGraphicOutput");

// * Define iterator variable
let i = 0;

// * Define graphic update logic
function updateBattery() {
    if (i <= 100) {
        battery.style.width = i + '%';
        batteryPercentage.innerHTML = i + '%';
        i++;
    } else {
        // clearInterval(intervalId); // Stop the interval when battery reaches 100%
        i = 0;
    }
}

// * Run updateBattery every {secondArgument ms}
const intervalId = setInterval(updateBattery, 100);