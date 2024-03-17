// * Battery Test Animation
// * Get HTML element objects for the % text and the graphic of battery.
const batteryPercentage = document.getElementById("batteryPercentageOutput");
const battery = document.getElementById("batteryGraphicOutput");
{
    // * Define iterator variable
    let i = 0;

    // * Define graphic update logic
    function updateBattery() {
        if (i <= 100) {
            battery.style.width = i + '%';
            batteryPercentage.innerHTML = '⚡' + i + '%';
            if (i === 100) {
                battery.style.backgroundColor = "lime";
            } else {
                // Change color as percentage increases
                const redValue = Math.floor((200 - 2*i) * 255 / 100);
                const greenValue = Math.floor(2 * i * 255 / 100);
                battery.style.backgroundColor = `rgb(${redValue}, ${greenValue}, 0)`;
            }
            i++;
        } else {
            i=0; // Stop the interval when battery reaches 100%
        }
}

// * Run updateBattery every {secondArgument ms}
setInterval(updateBattery, 100);
}