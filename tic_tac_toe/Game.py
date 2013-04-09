#!/usr/local/bin/python

import pysurface as p

def text_hover(obj, my_color=None):
	obj.Render("RenderUTF8_Shaded", color=my_color)

def text_hover(obj, my_color=None):
	obj.Render("RenderUTF8_Shaded", color=my_color)

def moveDot():
    dot.Properties(x=e.mouse_motion[0]-(dot.rect[2]/2), y=e.mouse_motion[1]-(dot.rect[3]))


Window = p.Display()
Window.Start()
e = p.Event(Window)


title_text = "Welcome to Tic Tac Toe Premium, by Robert Steckroth."

main_screen = p.Surface("box", width=-99, height=-99, color=0x969696)
Window.Position(main_screen, align="center")


title = p.Surface("font", font_size=22, font_text=title_text, path="fonts/Ubuntu-B.ttf")
title.Render("RenderUTF8_Blended", color=0x8f6b14)
main_screen.Position(title, align="center", padding=[50, 0, 0, 0])




game_area = p.Surface("box", width=main_screen.rect[2]-50, height=main_screen.rect[3]-50, color=0x133176)
main_screen.Position(game_area, align="center")

dot = p.Surface("image", path="images/x_lay_down.png")
main_screen.Position(dot)


Window.Position()


game_area.Hover(moveDot)

game_area.OnHover(game_area.Properties, color=0x30487e)
game_area.OffHover(game_area.Properties, color=0x133176)






def key_down_text():
  title.Render("RenderUTF8_Blended", color=0x8f1414, font_text="[ "+e.key_down+" ]  is not a recognized command.")

def key_up_text():
  title.Render("RenderUTF8_Blended", color=0x8f6b14, font_text=title_text)


Window.OnKeyDown(key_down_text)
Window.OnKeyUp(key_up_text)


while 1:
        # delay = how often the events are processed
        # event_cache = the maxuim number of events which are processed from to past
        # update_vars = Set to True if you want all of the event attributes updated according to triggered events,
        # 	(display width and height attributes will always be updated if one is attached).
    if e.GetNext(delay=10, event_cache=5, update_vars=False) == "quit":  # All arguments are optional. defaults(delay=10, event_cache=5, update_vars=False
	break # quit the program
          











