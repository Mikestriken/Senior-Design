import { fetchURL } from './modules.js';

{
    // * Create socket
    let socket = io.connect();
    let socketTopicOutdoorLight = "outdoor_light";
    let socketTopicIndoorLight = "indoor_light";
    let socketTopicFan = "fan";

    const fanSlider = document.querySelector('#fanSpeedSlider [type="range"]');
    const indoorLightPopOut = document.querySelector('#indoorLightPopOut');

    const indoorLightSlider = document.querySelector('#indoorLightSlider [type="range"]');
    const outdoorLightPopOut = document.querySelector('#outdoorLightPopOut');

    const outdoorLightSlider = document.querySelector('#outdoorLightSlider [type="range"]');
    const fanPopOut = document.querySelector('#fanPopOut');


    function updateRangeValue(numberOfStates, rangeSliderElement, popOutElement) {

        let rangePercent;

        switch (numberOfStates)
        {
            // * Must be On / Off
            case 2:
                // * States are 0, 1
                // * Percentages are: 0*100, 1*100 => 0%, 100%
                rangePercent = rangeSliderElement.value*100;
            
                switch (rangeSliderElement.value) {
                    case '0':
                        popOutElement.innerHTML = "OFF" + '<span></span>';
                        break;
                    case '1':
                        popOutElement.innerHTML = "ON" + '<span></span>';
                        break;
                }

                break;

            // * Only Fan slider has 3 states
            case 3:
                // * States are 0, 1, 2
                // * Percentages are: 0*50, 1*50, 2*50 => 0%, 50%, 100%
                rangePercent = rangeSliderElement.value*50;
            
                switch (rangeSliderElement.value) {
                    case '0':
                        popOutElement.innerHTML = "OFF" + '<span></span>';
                        break;
                    case '1':
                        popOutElement.innerHTML = "SLOW" + '<span></span>';
                        break;
                    case '2':
                        popOutElement.innerHTML = "FAST" + '<span></span>';
                        break;
                }

                break;
        }


        // rangeSliderElement.style.filter = 'hue-rotate(-' + rangePercent + 'deg)';
        popOutElement.style.transform = 'translateX(-50%) scale(' + (1 + ((rangePercent - (rangePercent/100)*70) / 100)) + ')';
        popOutElement.style.left = `${rangePercent}%`;
    }

    socket.on(socketTopicOutdoorLight, function (msg) {
        // * Convert JSON text → JavaScript Object
        // console.log(msg);

        switch(msg.toLowerCase()){
            case "is_off":
                outdoorLightSlider.value = 0;
                break;
            case "is_on":
                outdoorLightSlider.value = 1;
                break;
        }
        
        updateRangeValue(2, outdoorLightSlider, outdoorLightPopOut);
    });
    
    socket.on(socketTopicIndoorLight, function (msg) {
    // * Convert JSON text → JavaScript Object
    // console.log(msg);
    
        switch(msg.toLowerCase()){
            case "is_off":
                indoorLightSlider.value = 0;
                break;
            case "is_on":
                indoorLightSlider.value = 1;
                break;
        }
            
        updateRangeValue(2, indoorLightSlider, indoorLightPopOut);
    });
            
    socket.on(socketTopicFan, function (msg) {
        // * Convert JSON text → JavaScript Object
        // console.log(msg);
        
        switch(msg.toLowerCase()){
            case "is_off":
                fanSlider.value = 0;
                break;
            case "is_slow":
                fanSlider.value = 1;
                break;
            case "is_fast":
                fanSlider.value = 2;
                break;
        }
        
        updateRangeValue(3, fanSlider, fanPopOut);
    });

    function sliderEventHandler(rangeSliderElement) {
        switch (rangeSliderElement) {
            case fanSlider:
                fetchURL(`/fanSlider/${fanSlider.value}`);
                break;

            case indoorLightSlider:
                fetchURL(`/indoorLightSlider/${indoorLightSlider.value}`);
                break;

            case outdoorLightSlider:
                fetchURL(`/outdoorLightSlider/${outdoorLightSlider.value}`);
                break;
        }
    }

    // * Change triggers when mouse / touch is released from slider, input triggers as the slider moves across the bar for each value the slider passes.
    fanSlider.addEventListener('change', () => {updateRangeValue(3, fanSlider, fanPopOut); sliderEventHandler(fanSlider);});
    fanSlider.addEventListener('input', () => {updateRangeValue(3, fanSlider, fanPopOut);});
    indoorLightSlider.addEventListener('change', () => {updateRangeValue(2, indoorLightSlider, indoorLightPopOut); sliderEventHandler(indoorLightSlider);});
    indoorLightSlider.addEventListener('input', () => {updateRangeValue(2, indoorLightSlider, indoorLightPopOut);});
    outdoorLightSlider.addEventListener('change', () => {updateRangeValue(2, outdoorLightSlider, outdoorLightPopOut); sliderEventHandler(outdoorLightSlider);});
    outdoorLightSlider.addEventListener('input', () => {updateRangeValue(2, outdoorLightSlider, outdoorLightPopOut);});
}