from fgimage import FGImage
from graphics import Image
import appuifw2 as aw
from keycapture import KeyCapturer
import ui,kaapython

class Window:
    
    def __init__(s):
        s.capture = KeyCapturer(s.keys_answer)
        s.window = FGImage()
        try:
            s.layout = aw.app.layout(aw.EMainPane)
        except AttributeError:
            s.layout = ((176, 144), (0, 44))
        s.size = (s.layout[0][0], s.layout[0][1] + s.layout[1][1])
        s.imgnone = Image.new((1, 1))
        s.focusflag = 0
        s.resousce = None
        s.runing= 0
        s.initialization()

    def initialization(s):
        s.color_window = (255, 235, 200)
        s.color_outline = 0x00aa00
        s.color_cursor = (0, 0, 255)
        s.color_text = 0
        s.color_text_cursor = 0xffffff
        s.color_indicator = 0x8000
        try:
            s.callback = s.callback
        except AttributeError:
            s.callback = lambda:None

    def start(s, resousce):
        try:
            y = aw.app.body.pos2xy(aw.app.body.get_pos())[1]
        except AttributeError:
            return None
        s.y, s.z = 0, 0
        s.start_x=aw.app.body.get_pos()
        s.resousce = resousce
        if not s.resousce:
            return None
        elif type(s.resousce) == type([]):
            s.mode = 'list'
            s.list = s.resousce
        else:
            return None
        s.lenlist = len(s.list)
        center = s.size[1] / 2
        if aw.app.screen == 'normal':
            y += s.layout[1][1]
        if y >  center + 8:
            s.max_str_display = (y - 17) / 16
            s.imgsize = (s.size[0] - 10, min(s.max_str_display * 16, s.lenlist * 16))
            s.window_position = 5, 5
        else:
            s.max_str_display = (s.size[1] - y - 8) / 16
            s.imgsize = (s.size[0] - 10, min(s.max_str_display * 16, s.lenlist * 16))
            s.window_position = 5, max(y + 2, s.size[1] - s.imgsize[1] - 5)
        try:
            del s.img
        except AttributeError:
            pass
        s.img = Image.new(s.imgsize)
        s.capture.keys = [63497,63495,63496,63498,63557,63554,63555,63587,48]
        s.capture.forwarding = 0
        aw.app.focus = s.focus
        s.runing=1
        s.capture.start()
        s.picture()

    def result(s):
        s.runing= 0
        t= aw.app.body
        xt=t.get_pos()
        t.set_input_mode(ui.ENumericInputMode)
        t.delete(s.start_x,xt-s.start_x)
        t.set_pos(s.start_x)
        t.set_input_mode(ui.ETextInputMode)
        return unicode(s.list[s.y])
        

    def focus(s, f):
        if not f:
            s.window.unset()
            s.capture.stop()
        else:
            if s.focusflag:
                s.window.set(s.window_position[0], s.window_position[1], s.img._bitmapapi())
                s.capture.start()

    def stop(s):
            s.window.unset()
            s.capture.stop()
            s.focusflag = 0
            s.runing= 0

    def keys_answer(s, code):
        if code == 63498:#вниз
            if s.mode == 'list':
                s.y += 1
                if s.y == s.lenlist:
                    s.y = s.z = 0
                elif s.y - s.z == s.max_str_display:
                    s.z += 1
            else:
                if s.z < s.lenlist - s.max_str_display:
                    s.z += 1
        elif code == 63497:#вверх
            if s.mode == 'list':
                s.y -= 1
                if s.y < 0:
                    s.y = s.lenlist - 1
                    s.z = max(s.y - s.max_str_display + 1, 0)
                elif s.y < s.z:
                    s.z -= 1
            else:
                if s.z > 0:
                    s.z -= 1
        elif code == 63557:#ввод
            if s.mode == 'list':
                s.stop()
                s.callback()
                aw.e32.ao_yield()
                return None
        else:
            s.stop()
            return None
        s.picture()

    def picture(s):
        s.img.rectangle((0, 0, s.imgsize[0], s.imgsize[1]), s.color_outline, s.color_window)
        if s.mode == 'list':
            s.img.rectangle((1, (s.y - s.z) * 16 + 1, s.imgsize[0] - 1, (s.y - s.z) * 16 + 15), fill=s.color_cursor)
        a = 0
        for t in s.list[s.z:s.max_str_display + s.z]:
            if s.mode == 'list':
                if s.y - s.z == a:
                    color = s.color_text_cursor
                else:
                    color = s.color_text
            else:
                color = s.color_text
            s.img.text((3, a * 16 + 12),unicode(t), color, 'dense')
            a += 1
        if s.lenlist > s.max_str_display:
            s.img.rectangle((s.imgsize[0] - 5, 1, s.imgsize[0] - 1, s.imgsize[1] - 1), fill=s.color_window)
            s.img.rectangle((s.imgsize[0] - 4, s.z * (s.imgsize[1] - 2) / s.lenlist + 1, s.imgsize[0] - 2, s.z * (s.imgsize[1] - 2) / s.lenlist + max(s.max_str_display * (s.imgsize[1] - 2) / s.lenlist, 1) + 1), fill = s.color_indicator)
        s.window.set(s.window_position[0], s.window_position[1], s.img._bitmapapi())
        s.focusflag = 1
        
    def sort(s,mask):
        global w
        l=len(mask)
        sl1=[]
        no_name= 0
        for i in s.list:
            if i[0:l]==mask:
                sl1.insert(0,i)
                no_name=1
            else: sl1.append(i)
        s.list=sl1
        s.picture()
        


"""
moduls=[]
files_mod = os.listdir('e:\\resource\\')
for i in xrange(len(files_mod)):
    l=len(files_mod[i])
    if files_mod[i][l-4:l]==u'.pyd':
        moduls.append(files_mod[i][0:l-4])



help = Window()


exec('import sys')
func=dir(sys)
help.start(func)
"""






