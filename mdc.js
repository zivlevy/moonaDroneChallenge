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
        ws.send('3:7');
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

    // Move R Meters
    ext.moveRmeters = function(meters,callback) {
        ws.send('23:' + meters.toString());
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

    // Move L Meters
    ext.moveLmeters = function(meters,callback) {
        ws.send('24:' + meters.toString());
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

    // finf QR
    ext.findQR = function(id,callback) {
        ws.send('5:' + id.toString() );

        ws.onmessage = function (evt)
        {
            result = ""
            var received_msg = evt.data;
            var reader = new window.FileReader();
            reader.readAsBinaryString(received_msg);
            reader.onloadend = function() {
                result = reader.result;
                console.log(result );
                if (result=='FOUND') {
                    callback('FOUND');
                } else if (result=='WRONGQR'){
                    callback('WRONGQR');
                } else {
                    callback('NOQR');
                }
            }
        };
    };

    // TakePicture
    ext.takePicture = function(id,callback) {
        ws.send('6');

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

    // Set ISO
    ext.setISO = function(ISO,callback) {
        ws.send('30:' + ISO.toString());
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
            ['w', 'CONNECT %s', 'connect' , '10.0.0.253'],
            ['w', 'DISCONNECT', 'disconnect'],
            ['w', 'TAKEOFF', 'takeoff'],
            ['w', 'RTL', 'rtl'],
            ['w', 'LAND', 'land'],
            ['w', 'Set Heading %n', 'setheading',0],
            ['w', 'Forward %n meters', 'moveNmeters',1],
            ['w', 'Right %n meters', 'moveRmeters',1],
            ['w', 'Left %n meters', 'moveLmeters',1],
            ['w', 'Set ISO %n', 'setISO',100],
            ['R', 'Find QR ID %n', 'findQR',1000],
            ['w', 'Take Picture', 'takePicture']
        ]
    };

    // Register the extension
    ScratchExtensions.register('Moona Drone Challenge', descriptor, ext);
    console.log ('new ws');
    var ws;





})({});
