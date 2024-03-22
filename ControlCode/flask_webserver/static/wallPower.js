{
    // * Create object on html subdirectory to register events on
    const eventSource = new EventSource('/wall-power-events');
    
    const powerStatusOutput = document.getElementById('powerStatusOutput');

    eventSource.onmessage = function(event) {
        // * Convert JSON text → JavaScript Object
        console.log(event);
        const jsonData = JSON.parse(event.data);

        // * Set powerStatusOutput background color accordingly...
        if ( jsonData.wall_power === "Wall Power Disconnected!" )
            powerStatusOutput.style.backgroundColor = "red";

        else if (jsonData.wall_power === "Wall Power Reconnected!")
            powerStatusOutput.style.backgroundColor = "lime";
    }
}