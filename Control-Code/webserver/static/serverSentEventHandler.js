// * Create object on html subdirectory to register events on
const eventSource = new EventSource('/events');

// * Define textField Object
const textField = document.getElementById('textField');

const windSpeedOutput = document.getElementById('windSpeedOutput');
const windDirectionOutput = document.getElementById('windDirectionOutput');

const externalTemperatureOutput = document.getElementById('externalTemperatureOutput');
const pressureOutputHG = document.getElementById('pressureOutputHG');
const pressureOutputBar = document.getElementById('pressureOutputBar');
const humidityOutput = document.getElementById('humidityOutput');
const dewPointOutput = document.getElementById('dewPointOutput');

// * Define an event handler to resolve these "interrupts"
eventSource.onmessage = function(event) {
  // * Convert JSON text → JavaScript Object
  console.log(event);
  const jsonData = JSON.parse(event.data);
  
  // * heading
    // * Update the webpage with the received JSON data
    // textField.value = `Timestamp: ${jsonData.timestamp}, Value: ${jsonData.value}`;
    textField.value = `The Weather Station is Currently Pointing: ${jsonData.weather_data.heading}°`;

  // * wind
    windSpeedOutput.innerHTML = jsonData.weather_data.wind.speed;
    windDirectionOutput.innerHTML = jsonData.weather_data.wind.direction;

  // * meteorological
    pressureOutputHG.innerHTML = jsonData.weather_data.meteorological.pressureMercury;
    pressureOutputBar.innerHTML = jsonData.weather_data.meteorological.pressureBars;
    externalTemperatureOutput.innerHTML = jsonData.weather_data.meteorological.temperature;
    humidityOutput.innerHTML = jsonData.weather_data.meteorological.humidity;
    dewPointOutput.innerHTML = jsonData.weather_data.meteorological.dewPoint;
  
};