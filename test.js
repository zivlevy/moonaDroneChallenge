(function(ext) {
 // Cleanup function when the extension is unloaded
 ext._shutdown = function() {};
 
 // Status reporting code
 // Use this to report missing hardware, plugin or unsupported browser
 ext._getStatus = function() {
 return {status: 2, msg: 'Ready'};
 };
 
 // Functions for block with type 'w' will get a callback function as the
 // final argument. This should be called to indicate that the block can
 // stop waiting.
 ext.wait_random = function(callback) {
 wait = Math.random();
 console.log('Waiting for ' + wait + ' seconds');
 window.setTimeout(function() {
                   callback();
                   }, wait*1000);
 };
 
 ext.WebSocketTest = function ()
 {
    if ("WebSocket" in window)
        {
            alert("WebSocket is supported by your Browser!");
 
             // Let us open a web socket
             var ws = new WebSocket("ws://127.0.0.1:9988");
             
             ws.onopen = function()
             {
             // Web Socket is connected, send data using send()
             ws.send("Message to send");
             alert("Message is sent...");
             };
             
             ws.onmessage = function (evt)
             {
             var received_msg = evt.data;
             alert("Message is received...");
             };
             
             ws.onclose = function()
             {
                // websocket is closed.
                alert("Connection is closed...");
            }
    } else {
     // The browser doesn't support WebSocket
     alert("WebSocket NOT supported by your Browser!");
     }
 };
 
 // Block and block menu descriptions
 var descriptor = {
 blocks: [
          ['w', 'takeoff', 'WebSocketTest'],
          ['w', 'LAND', 'wait_random'],
          ]
 };
 
 // Register the extension
 ScratchExtensions.register('Random wait extension', descriptor, ext);
 })({});