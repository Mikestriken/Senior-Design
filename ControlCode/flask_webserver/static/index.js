{
    const windSpeedOutput = document.getElementById('windSpeedOutput');
    const windDirectionOutput = document.getElementById('windDirectionOutput');
    const windDirectionUnit = document.getElementById('windDirectionUnit');
  
    const externalTemperatureOutput = document.getElementById('externalTemperatureOutput');
    const pressureOutputHG = document.getElementById('pressureOutputHG');
    const pressureOutputBar = document.getElementById('pressureOutputBar');
    const humidityOutput = document.getElementById('humidityOutput');
    const dewPointOutput = document.getElementById('dewPointOutput');
  
    const internalTemperatureOutput = document.getElementById('internalTemperatureOutput');

    const powerStatusOutput = document.getElementById('powerStatusOutput');
  
    // Function to generate random integer with one decimal point precision
    function getRandomInt() {
      return Math.floor(Math.random() * 900 + 1000) / 10; // Generates random number between 100 and 999 with one decimal point precision
    }
  
    // Set random values for each output
    function randomize() {
      windSpeedOutput.innerHTML = getRandomInt();
      // windDirectionOutput.innerHTML = getRandomInt();
      let direction = getRandomInt()
      if (direction >= -22.5 && direction <= 22.5) { // North
        windDirectionOutput.innerHTML = direction;
        windDirectionUnit.innerHTML = "N";
      } 
      
      else if (direction > 22.5 && direction < 67.5) { // North East
        windDirectionOutput.innerHTML = direction;
        windDirectionUnit.innerHTML = "NE";
      }
      
      else if (direction >= 67.5 && direction <= 112.5) { // East
        windDirectionOutput.innerHTML = direction;
        windDirectionUnit.innerHTML = "E";
      } 
      
      else if (direction > 112.5 && direction < 157.5) { // South East
        windDirectionOutput.innerHTML = direction;
        windDirectionUnit.innerHTML = "SE";
      }
      
      else if (direction >= 157.5 && direction <= 202.5) { // South
        windDirectionOutput.innerHTML = direction;
        windDirectionUnit.innerHTML = "S";
      } 
      
      else if (direction > 202.5 && direction < 247.5) { // South West
        windDirectionOutput.innerHTML = direction;
        windDirectionUnit.innerHTML = "SW";
      }
      
      else if (direction >= 247.5 && direction <= 292.5) { // West
        windDirectionOutput.innerHTML = direction;
        windDirectionUnit.innerHTML = "W";
      } 
      
      else if (direction > 292.5 && direction < 337.5) { // North West
        windDirectionOutput.innerHTML = direction;
        windDirectionUnit.innerHTML = "NW";
      }
      
      else if (direction >= 337.5 && direction <= 382.5) { // North
        windDirectionOutput.innerHTML = direction;
        windDirectionUnit.innerHTML = "N";
      }
      
      else {
        windDirectionOutput.innerHTML = direction;
        windDirectionUnit.innerHTML = "UNK";
      }
      externalTemperatureOutput.innerHTML = getRandomInt();
      
      pressureOutputHG.innerHTML = getRandomInt();
      pressureOutputBar.innerHTML = getRandomInt();
      humidityOutput.innerHTML = getRandomInt();
      dewPointOutput.innerHTML = getRandomInt();
      
      internalTemperatureOutput.innerHTML = getRandomInt();

      if (powerStatusOutput.style.backgroundColor === "lime")
        powerStatusOutput.style.backgroundColor = "red";
      else
        powerStatusOutput.style.backgroundColor = "lime";
    }
  
  
    // * Run update every {secondArgument ms}
    //setInterval(randomize, 1000);
  }