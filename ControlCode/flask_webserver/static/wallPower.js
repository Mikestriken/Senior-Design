{
    // * Create socket
    let socket = io.connect();
    let socketTopic = "wall_power";
    
    const powerStatusOutput = document.getElementById('powerStatusOutput');
    
    socket.on(socketTopic, function (msg) {
        // * Convert JSON text → JavaScript Object
        console.log(msg);
        const data = msg;
    
        // * Set powerStatusOutput background color accordingly...
        if ( data.toLowerCase() === "Wall Power Disconnected!".toLowerCase() )
            powerStatusOutput.style.backgroundColor = "red";
  
        else if ( data.toLowerCase() === "Wall Power Reconnected!".toLowerCase() )
            powerStatusOutput.style.backgroundColor = "lime";
      });
}