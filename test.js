(function(ext) {
    // Code to be run when the user closes the window, reloads the page, etc.    
    ext._shutdown = function() {};
    
    // Shows the status of the extension 0 = red, 1 = yellow, and 2 = green
    ext._getStatus = function() {
        return {status: 2, msg: 'Ready'};
    };
    // Descriptions of the blocks and menus the extension adds
    var descriptor = {
blocks: [
        ['w', ‘takeoff to alt %n meters’,             'motorOnFor', 1],
        [' ', 'turn motor on',                         'allMotorsOn'],
        [' ', 'turn motor off',                        'allMotorsOff'],
        [' ', 'set motor power %n',                    'startMotorPower', 100],
        [' ', 'set motor direction %m.motorDirection', 'setMotorDirection', 'this way'],
        ['h', 'when distance %m.lessMore %n',          'whenDistance', '<', 20],
        ['h', 'when tilt %m.eNe %n',                   'whenTilt', '=', 1],
        ['r', 'distance',                              'getDistance'],
        ['r', 'tilt',                                  'getTilt']
    ],
    menus: {
        motorDirection: ['this way', 'that way', 'reverse'],
        lessMore: ['<', '>'],
        eNe: ['=','not =']
    },
    url: 'http://info.scratch.mit.edu/WeDo'
    };
    // Register the extension
    ScratchExtensions.register('Hello World', descriptor, ext);
})({});