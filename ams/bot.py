import time

from ams.loggable import Loggable

import re
POS = re.compile(r'Count X: (?P<x>\d+.\d\d) Y:(?P<y>\d+.\d\d) Z:(?P<z>\d+.\d\d)')
class Bot(Loggable):
    name = 'Bot'
    _cx = None
    _cy = None
    _cz = None
    
    def __init__(self, sender):
        self._sender = sender
        
    def home(self):
        self._sender.send('G28')
        self.block()
        
        
    def block(self):
        while 1:
            ret = self.getstatus()
            if ret:
                break
            time.sleep(0.1)
       
    def getstatus(self):
        msg = self._sender.send('\r')
        print('status', msg)
        return msg == b'ok\r\n'
        
    def moveto(self, x, y, z=None, rate=1000):
        
        cmd = f'G0 F{rate} X{x} Y{y}'
        if z is not None:
            cmd = f'{cmd} Z{z}'
            
        self._sender.send(cmd)
        
        if z is None:
            z = 0
            
        if not self._cx:
            wait = 5
        else:
            if float(z)!=self._cz:
                wait=5
            else:
                d = ((self._cx-float(x))**2+(self._cy-float(y))**2)**0.5
                wait = d/rate*60

        self._cx,self._cy,self._cz = float(x), float(y), float(z)
        time.sleep(wait)
             
            
    def move_rel(self):
        self._sender.send('G91')
        
    def move_abs(self):
        self._sender.send('G90')
        

        
