{
    // * Create socket
    let socket = io.connect();
    let socketTopic = "wall_power";
    
    const powerStatusOutput = document.getElementById('powerStatusOutput');
    
    socket.on(socketTopic, function (msg) {
        // * Convert JSON text → JavaScript Object
        // console.log(msg[socketTopic]);
        const data = msg;
    
        // * Set powerStatusOutput background color accordingly...
        if ( data[socketTopic] === "Wall Power Disconnected!" )
            powerStatusOutput.style.backgroundColor = "red";
  
        else if (data[socketTopic] === "Wall Power Reconnected!")
            powerStatusOutput.style.backgroundColor = "lime";
      });
}