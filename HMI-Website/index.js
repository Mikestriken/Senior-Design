const batteryPercentage = document.getElementById("batteryPercentageOutput");
const battery = document.getElementById("batteryGraphicOutput");

let i = 0;

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

const intervalId = setInterval(updateBattery, 100); // Run updateBattery every 1000 milliseconds

/* for (let i=0; i<=100; ++i)
{
    setInterval(function(){
        battery.style.width = i + '%';
        batteryPercentage.innerHTML = i + '%';
    },1000);
} */