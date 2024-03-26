{
    // * Create socket
    let socket = io.connect();
    let socketTopic = "weather";
  
    const windSpeedOutput = document.getElementById('windSpeedOutput');
    const windDirectionOutput = document.getElementById('windDirectionOutput');
    const windDirectionUnit = document.getElementById('windDirectionUnit');
  
    const externalTemperatureOutput = document.getElementById('externalTemperatureOutput');
    const pressureOutputHG = document.getElementById('pressureOutputHG');
    const pressureOutputBar = document.getElementById('pressureOutputBar');
    const humidityOutput = document.getElementById('humidityOutput');
    const dewPointOutput = document.getElementById('dewPointOutput');
    
    socket.on(socketTopic, function (msg) {
        // * Convert JSON text → JavaScript Object
        // console.log(msg[socketTopic]);
        const data = msg;
  
        // * wind
          windSpeedOutput.innerHTML = data[socketTopic].wind.speed;
    
          let direction = data[socketTopic].wind.trueDirection
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
          
    
        // * meteorological
          pressureOutputHG.innerHTML = data[socketTopic].meteorological.pressureMercury;
          pressureOutputBar.innerHTML = data[socketTopic].meteorological.pressureBars;
          externalTemperatureOutput.innerHTML = data[socketTopic].meteorological.temperature;
          humidityOutput.innerHTML = data[socketTopic].meteorological.humidity;
          dewPointOutput.innerHTML = data[socketTopic].meteorological.dewPoint;
      });
  }