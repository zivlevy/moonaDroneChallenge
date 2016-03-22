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
        ws = new WebSocket("ws://10.0.0.17:8000");
        ws.onopen = function()
        {
            alert("Socket open.");
        };

        ws.onmessage = function (evt)
        {
            var received_msg = evt.data;
            //alert("Message is received..." + received_msg);

        };

        ws.onclose = function()
        {
            // websocket is closed.
            alert("Connection is closed...");
        };
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
        ws.send('3:5');
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

    //  Set Heading
    ext.setheading = function(heading,callback) {
        console.log(heading);
        ws.send('12:' + heading.toString());
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

    // Move N Meters
    ext.moveNmeters = function(meters,callback) {
        ws.send('11:' + meters.toString() +':0:0');
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

    // Move N Meters North
    ext.moveNmetersNorth = function(meters,callback) {
        ws.send('22:' + meters.toString() +':0:0');
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

    // Move N Meters South
    ext.moveNmetersSouth = function(meters,callback) {
        ws.send('23:' + meters.toString() +':0:0');
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

    // Move N Meters East
    ext.moveNmetersEast = function(meters,callback) {
        ws.send('24:' + meters.toString() +':0:0');
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

    // Move N Meters Weat
    ext.moveNmetersWest = function(meters,callback) {
        ws.send('25:' + meters.toString() +':0:0');
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
    // TakePicture
    ext.takePicture = function(callback) {
        ws.send('5');
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
            ['w', 'Left 5', 'left5'],
            ['w', 'Set Heading %n', 'setheading',360],
            ['w', 'Move %n meters', 'moveNmeters',1],
            ['w', 'Take picture', 'takePicture'],
            ['w', 'Move %n meters north ', 'moveNmetersNorth',1],
            ['w', 'Move %n meters east', 'moveNmetersEast',1],
            ['w', 'Move %n meters south', 'moveNmetersSouth',1],
            ['w', 'Move %n meters west', 'moveNmetersWest',1],
        ]
    };

    // Register the extension
    ScratchExtensions.register('Moona Drone Challenge', descriptor, ext);
    console.log ('new ws');
    var ws;





})({});
