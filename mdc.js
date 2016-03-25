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
    ext.connect = function (ip, callback) {
        alert ('Connect send');
        a = "ws://";
        b=":8000";
        wsAddress = a+ip+b;
        ws = new WebSocket(wsAddress);
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
        ws.send('22:' + meters.toString());
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
    ext.takePicture = function(id,callback) {
        ws.send('5:' + id.toString() );
        ws.onmessage = function (evt)
        {
            var received_msg = evt.data;
            console.log(received_msg.toString())
            if (received_msg=='FOUND') {
                callback('FOUND');
            } else if (received_msg=='WRONGQR'){
                callback('WRONGQR');
            } else {
                callback('NOQR');
            }

        };
    };
    // Block and block menu descriptions
    var descriptor = {
        blocks: [
            ['w', 'CONNECT %s', 'connect' , '10.0.0.253'],
            ['w', 'DISCONNECT', 'disconnect'],
            ['w', 'TAKEOFF', 'takeoff'],
            ['w', 'RTL', 'rtl'],
            ['w', 'LAND', 'land'],
            ['w', 'Set Heading %n', 'setheading',0],
            ['R', 'Find QR ID %n', 'takePicture',1000],
            ['w', 'Move %n meters', 'moveNmeters',1]
        ]
    };

    // Register the extension
    ScratchExtensions.register('Moona Drone Challenge', descriptor, ext);
    console.log ('new ws');
    var ws;





})({});
