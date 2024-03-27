{
    // * Create socket
    let socket = io.connect();
    let socketTopicOutdoor = "outdoor_weather";
    let socketTopicIndoor = "indoor_weather";
  
    const windSpeedOutput = document.getElementById('windSpeedOutput');
    const windDirectionOutput = document.getElementById('windDirectionOutput');
    const windDirectionUnit = document.getElementById('windDirectionUnit');
  
    const externalTemperatureOutput = document.getElementById('externalTemperatureOutput');
    const pressureOutputHG = document.getElementById('pressureOutputHG');
    const pressureOutputBar = document.getElementById('pressureOutputBar');
    const humidityOutput = document.getElementById('humidityOutput');
    const dewPointOutput = document.getElementById('dewPointOutput');

    const internalTemperatureOutput = document.getElementById('internalTemperatureOutput');
    
    socket.on(socketTopicOutdoor, function (msg) {
      // * Convert JSON text → JavaScript Object
      // console.log(msg[socketTopicOutdoor]);
      const data = msg;
  
      // * wind
      windSpeedOutput.innerHTML = data[socketTopicOutdoor].wind.speed;
      
      let direction = data[socketTopicOutdoor].wind.trueDirection
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
          pressureOutputHG.innerHTML = data[socketTopicOutdoor].meteorological.pressureMercury;
          pressureOutputBar.innerHTML = data[socketTopicOutdoor].meteorological.pressureBars;
          externalTemperatureOutput.innerHTML = data[socketTopicOutdoor].meteorological.temperature;
          humidityOutput.innerHTML = data[socketTopicOutdoor].meteorological.humidity;
          dewPointOutput.innerHTML = data[socketTopicOutdoor].meteorological.dewPoint;

        });

        socket.on(socketTopicIndoor, function (msg) {
          // * Convert JSON text → JavaScript Object
          // console.log(msg[socketTopicIndoor]);
          const data = msg;

          internalTemperatureOutput.innerHTML = data[socketTopicIndoor].temperature;
        });
  }