from __future__ import annotations
import math
from dataclasses import dataclass

@dataclass
class Vec2:
    x: float = 0.0
    y: float = 0.0
    def __add__(self, o): return Vec2(self.x+o.x, self.y+o.y)
    def __sub__(self, o): return Vec2(self.x-o.x, self.y-o.y)
    def __mul__(self, s): return Vec2(self.x*s, self.y*s) if isinstance(s,(int,float)) else Vec2(self.x*s.x, self.y*s.y)
    def length(self): return math.hypot(self.x, self.y)
    def normalized(self): l=self.length(); return Vec2(self.x/l, self.y/l) if l!=0 else Vec2()
    def to_tuple(self): return (self.x, self.y)

@dataclass
class Vec3:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    def __add__(self, o): return Vec3(self.x+o.x, self.y+o.y, self.z+o.z)
    def __sub__(self, o): return Vec3(self.x-o.x, self.y-o.y, self.z-o.z)
    def __mul__(self, s): return Vec3(self.x*s, self.y*s, self.z*s)
    def length(self): return math.sqrt(self.x*self.x+self.y*self.y+self.z*self.z)
    def to_tuple(self): return (self.x,self.y,self.z)

@dataclass
class Vec4:
    x: float=0; y: float=0; z: float=0; w: float=0
    def to_tuple(self): return (self.x,self.y,self.z,self.w)

class Mat4:
    def __init__(self, cols=None):
        self.cols = cols or [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
    @staticmethod
    def identity(): return Mat4()
    @staticmethod
    def translate(v: Vec3): m=Mat4(); m.cols[3]=[v.x,v.y,v.z,1]; return m
    def __repr__(self): return f"Mat4({self.cols})"
