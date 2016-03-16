(function(ext) {
    // Cleanup function when the extension is unloaded
    ext._shutdown = function() {
        ws.close();
    };

    // Status reporting code
    // Use this to report missing hardware, plugin or unsupported browser
    ext._getStatus = function() {
        return {status: 2, msg: 'Ready'};
    };

    // Functions for block with type 'w' will get a callback function as the
    // final argument. This should be called to indicate that the block can
    // stop waiting.
    ext.land = function(callback) {
        alert('Land sent');
        ws.send('9');
        ws.onmessage = function (evt)
        {
            var received_msg = evt.data;
            if (received_msg=='ACK') {
                callback('ACK');
            } else {
                callback('FAIL');
            }

        };
    };

    ext.takeoff = function (callback) {

        alert ('Takeoff sent');
        ws.send('3:100');
        ws.onmessage = function (evt)
        {
            var received_msg = evt.data;
            if (received_msg=='ACK') {
                callback('ACK');
            } else {
                callback('FAIL');
            }

        };

    };

    // Block and block menu descriptions
    var descriptor = {
        blocks: [
            ['w', 'TAKEOFF', 'takeoff'],
            ['w', 'LAND', 'land']
        ]
    };

    // Register the extension
    ScratchExtensions.register('Moona Drone Challenge', descriptor, ext);
    console.log ('new ws');
    var ws = new WebSocket("ws://10.0.1.253:8000");


    ws.onopen = function()
    {

        alert("Socket open.");
    };

    ws.onmessage = function (evt)
    {
        var received_msg = evt.data;
        alert("Message is received..." + received_msg);

    };

    ws.onclose = function()
    {
        // websocket is closed.
        alert("Connection is closed...");
    };


})({});
