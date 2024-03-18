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

fanSlider.addEventListener('change', () => {updateRangeValue(3, fanSlider, fanPopOut);});
fanSlider.addEventListener('input', () => {updateRangeValue(3, fanSlider, fanPopOut);});
indoorLightSlider.addEventListener('change', () => {updateRangeValue(2, indoorLightSlider, indoorLightPopOut);});
indoorLightSlider.addEventListener('input', () => {updateRangeValue(2, indoorLightSlider, indoorLightPopOut);});
outdoorLightSlider.addEventListener('change', () => {updateRangeValue(2, outdoorLightSlider, outdoorLightPopOut);});
outdoorLightSlider.addEventListener('input', () => {updateRangeValue(2, outdoorLightSlider, outdoorLightPopOut);});