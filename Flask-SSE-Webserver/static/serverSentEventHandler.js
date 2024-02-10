// * Create object on html subdirectory to register events on
const eventSource = new EventSource('/events');

// * Define textField Object
const textField = document.getElementById('textField');

// * Define an event handler to resolve these "interrupts"
eventSource.onmessage = function(event) {
  // * Convert JSON text → JavaScript Object
  console.log(event);
  const jsonData = JSON.parse(event.data);
  
  // * Update the webpage with the received JSON data
  textField.value = `Timestamp: ${jsonData.timestamp}, Value: ${jsonData.value}`;
};