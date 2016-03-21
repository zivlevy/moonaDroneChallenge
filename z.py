print "Starting copter simulator (SITL)"
from dronekit_sitl import SITL
sitl = SITL()
sitl.download('copter', '3.2.1', verbose=True)
sitl_args = ['-I0', '--model', 'quad', '--home=-35.363261,149.165230,584,353']
sitl.launch(sitl_args, await_ready=True, restart=True)
connection_string='tcp:127.0.0.1:5760'
