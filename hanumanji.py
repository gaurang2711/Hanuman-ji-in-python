import turtle as tu
import cv2
from svgpathtools import svg2paths2
from svg.path import parse_path
from tqdm import tqdm
class sketch_from_svg:

    def __init__(self,path,scale=30,x_offset=350,y_offset=350):

        self.path = path
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.scale = scale

    def hex_to_rgb(self,string):
        strlen = len(string)
        if string.startswith('#'):
            if strlen == 7:
                r = string[1:3]
                g = string[3:5]
                b = string[5:7]
            elif strlen == 4:
                r = string[1:2]*2
                g = string[2:3]*2
                b = string[3:4]*2
        elif strlen == 3:
                r = string[0:1]*2
                g = string[1:2]*2
                b = string[2:3]*2
        else:
            r = string[0:2]
            g = string[2:4]
            b = string[4:6]
        
        return int(r,16)/255,int(g,16)/255, int(b,16)/255

    

    def load_svg(self):
        print('loading data')
        paths,attributes,svg_att = svg2paths2(self.path)
        h = svg_att["height"]
        w = svg_att['width']
        self.height = int(h[:h.find('.')])
        self.width = int(w[:w.find('.')])

        res = []
        for i in tqdm(attributes):
            path = parse_path(i['d'])
            co = i['fill']
            #print(co)
            col = self.hex_to_rgb(co)
            #print(col)
            n = len(list(path))+2       
            pts = [((int((p.real/self.width)*self.scale))-self.x_offset, (int((p.imag/self.height)*self.scale))-self.y_offset) for p in (path.point(i/n) for i in range(0,n+1))]
            res.append((pts,col))
            #res.append(pts)
        print('svg data loaded')
        return res

    def move_to(self,x, y):
        self.pen.up()
        self.pen.goto(x,y)
        self.pen.down()


    def draw(self,retain=True):
        coordinates = self.load_svg()
        self.pen = tu.Turtle()
        self.pen.speed(0)
        for path_col in coordinates:
            f = 1
            self.pen.color('black')
            #print(path_col)
            path = path_col[0]
            #print(path_col)
            col = path_col[1]
            #print(col)
            self.pen.color(col)
            self.pen.begin_fill()
            next = 0
            for coord in path:
                #for coord in path_col:
                x,y = coord
                y *= -1
                #print(x,y)
                if f:
                    self.move_to(x, y)
                    f=0
                else:
                    self.pen.goto(x,y)
            self.pen.end_fill()

        if retain == True:
            tu.done()
pen= sketch_from_svg('2022_07_17.svg',scale=70)
pen.draw()







