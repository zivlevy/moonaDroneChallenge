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


// CONNECT
    ext.connect = function (callback) {
        alert ('Connect send');
        ws = new WebSocket("ws://10.0.1.253:8000");
        callback('ACK');

    };
// DISCONNECT
    ext.disconnect = function (callback) {
        ws.disconnect();
        callback('ACK');

    };

// TAKOFF
    ext.takeoff = function (callback) {
        alert ('Takeoff sent');
        ws.send('3:10');
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

    // RTL
    ext.rtl = function(callback) {
        alert('RTL sent');
        ws.send('8');
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

    // LAND
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

    // Forward 5
    ext.forward5 = function(callback) {
        ws.send('11:5:0:0');
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

    // Back 5
    ext.back5 = function(callback) {
        ws.send('11:-5:0:0');
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

    // Right 5
    ext.right5 = function(callback) {
        ws.send('11:0:5:0');
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

    // Left 5
    ext.left5 = function(callback) {
        ws.send('11:0:-5:0');
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
            ['w', 'CONNECT', 'connect'],
            ['w', 'DISCONNECT', 'disconnect'],
            ['w', 'TAKEOFF', 'takeoff'],
            ['w', 'RTL', 'rtl'],
            ['w', 'LAND', 'land'],
            ['w', 'Forward 5', 'forward5'],
            ['w', 'Back 5', 'back5'],
            ['w', 'Right 5', 'right5'],
            ['w', 'Left 5', 'left5']
        ]
    };

    // Register the extension
    ScratchExtensions.register('Moona Drone Challenge', descriptor, ext);
    console.log ('new ws');
    var ws;


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
