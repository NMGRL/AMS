import time
from ams.loggable import Loggable
import os


class Mosaic(Loggable):
    name = 'mosaic'
    def __init__(self, cam, bot):
        self._cam = cam
        self._bot = bot
        
        
        self._xsteps = 5
        self._ysteps = 5
        
        self._xorigin = 25
        self._yorigin = 5
        self._zorigin = 29.15
        
        self._xstep_size = 5
        self._ystep_size = 5
        
        
    def run(self):
        self._bot.move_abs()
        self._bot.moveto(self._xorigin,self._yorigin, self._zorigin)
        root = './data/mosaic'
        for yi in range(self._ysteps):
            for xi in range(self._xsteps):
                
                self._move(xi+1,yi+1)
                time.sleep(2)
                name = f'img{yi:03n}_{xi:03n}.png'
                path = os.path.join(root, name)
                self._cam.capture(path)                 
                time.sleep(2)
            
                
    def _move(self, x, y, z=None):
        
        x = self._xorigin + self._xstep_size*x
        y = self._yorigin + self._ystep_size*y
        
        self._bot.moveto(x,y, z)

