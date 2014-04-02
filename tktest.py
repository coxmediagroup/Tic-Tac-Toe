#!/usr/bin/python

from Tkinter import Tk, Frame, Button
from ttk import Style, Label, Entry

class Example(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent, background="white")
		self.parent = parent
		self.buttons = []
		self.initUI()

	def initUI(self):
		self.parent.title("Buttons")
		buttons = []
		Style().configure("TButton", font="serif 128")

		self.columnconfigure(0, pad=3)
		self.columnconfigure(1, pad=3)
		self.columnconfigure(2, pad=3)

		self.rowconfigure(0, pad=3)
		self.rowconfigure(1, pad=3)
		self.rowconfigure(2, pad=3)

		#entry = Entry(self)
		#entry.grid(row=0, columnspan=3, sticky=W+E)
		
		for x in range(9):
			handler = lambda x=x:self.makeMove(x)
			self.buttons.append(Button(self,command=handler,text='X',height=4,width=4))
			self.buttons[-1].grid(row=(x / 3), column=(x % 3))

		"""
		one = Button(self,text="-")
		one.grid(row=1,column=0)
		two = Button(self,text="-")
		two.grid(row=1,column=1)
		thr = Button(self,text="-")
		thr.grid(row=1,column=2)

		fou = Button(self,text="-")
		fou.grid(row=2,column=0)
		fiv = Button(self,text="-")
		fiv.grid(row=2,column=1)
		six = Button(self,text="-")
		six.grid(row=2,column=2)

		sev = Button(self,text="-")
		sev.grid(row=3,column=0)
		eig = Button(self,text="-")
		eig.grid(row=3,column=1)
		nine = Button(self,text="-")
		nine.grid(row=3,column=2)
		"""
		self.pack()
	
	def makeMove(self, input):
		self.buttons[input]['text']=input
		#quitButton = Button(self, text="Quit", command=self.quit)
		#quitButton.place(x=50,y=50)

def main():
	root = Tk()
	root.geometry("250x250+300+300")
	app = Example(root)
	root.mainloop()

if __name__ == '__main__':
	main()
