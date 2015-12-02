import threading
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter.messagebox import showerror
from printClient import *


class MyFrame(Frame):
	def __init__(self):
		Frame.__init__(self)
		# threading.Thread.__init__(self)

		self.master.title("DF Print Studio Test")
		# self.master.geometry('600x400')
		self.master.rowconfigure(0, weight=1)
		self.master.columnconfigure(0, weight=1)
		# self.master.configure(bg='blue')
		# self.master.attributes('-alpha', 0.96)
		self.grid(sticky=W+E+N+S)
		self.gcode = ''
		self.transformData = [[1, 0, 0, -9],[0, 1, 0, -9],[0, 0, 1, 0]]

		self.inputFrame = Frame(self)
		# self.inputFrame.grid(row=0, column=0, sticky="eswn")
		self.inputFrame.pack(side=LEFT, fill=BOTH,padx=3, pady=3)

		self.buttonFrame = Frame(self.inputFrame)
		self.buttonFrame.grid(row=0,column=0, sticky=W) 
		self.loadButton = Button(self.buttonFrame, text="open STL file", command=self.load_file)
		self.loadButton.pack(side=LEFT, expand=YES)
		self.loadButton.state = 'DISABLED'

		# self.buildButton = Button(self.buttonFrame, text="build", command=self.build_gcode)
		# self.buildButton.pack(side=LEFT, expand=YES, fill=BOTH)

		self.saveButton = Button(self.buttonFrame, text="save gcode", command=self.save_file)
		self.saveButton.pack(side=LEFT, expand=YES)

		self.printer_id_e = StringVar()
		self.printer_id_label = Label (self.inputFrame, width=11, text = "printer-type-id:", anchor = W)
		self.printer_id_label.grid(row=1, column=0, sticky=W)
		self.printer_id = Entry(self.inputFrame, width=34, textvariable=self.printer_id_e)
		self.printer_id.grid(row=2, column=0, rowspan=1, columnspan=3, sticky=W)
		self.printer_id_e.set('4A0F7523-071B-4F1E-A527-9DA49AECB807')

		self.profile_e = StringVar()
		self.profile_label = Label (self.inputFrame, width=11, text = "profile-id:", anchor=W)
		self.profile_label.grid(row=3, column=0, sticky=W)
		self.profile = Entry(self.inputFrame, width=34, textvariable=self.profile_e)
		self.profile.grid(row=4, column=0, rowspan=1, columnspan=3, sticky=W)
		self.profile_e.set('EF6D5047-0D09-4F6A-AC06-9EF09638D2C9')


		self.transform_label = Label (self.inputFrame, width=11, text = "transform:", anchor=W)
		self.transform_label.grid(row=5, column=0, sticky=W)

		self.form = Frame (self.inputFrame, width = 100, height=100)
		self.form.grid(row=6, column=0, rowspan=1, columnspan=1, sticky=W)

		self.prepareTrayLabel= Label(self.inputFrame, text="prepareTrayProgress")
		self.prepareTrayLabel.grid(row=7, column=0, sticky=W)

		self.generateGcodeLabel = Label(self.inputFrame, text="generateGcodeProgress")
		self.generateGcodeLabel.grid(row=8, column=0, sticky=W)

		self.entry = []
		self.e = []

		for i in range(12):
			self.e.append(StringVar())
			self.entry.append(Entry(self.form, width=3, textvariable=self.e[i]))
		for i in range(3):
			for j in range(4):
				self.entry[i*4+j].grid(row=i, column=j, rowspan=1, columnspan=1)
				self.e[i*4+j].set (self.transformData[i][j])

		self.frameText = LabelFrame(self, text="Gcode")
		# self.frameText.grid(row=0, column=1, sticky="eswn")
		self.frameText.pack(side=LEFT, expand=YES, fill=BOTH, padx=3, pady=3)
		self.scrollbar = Scrollbar(self.frameText)
		self.scrollbar.pack(side=RIGHT, fill=BOTH)
		self.code = Text(self.frameText, yscrollcommand = self.scrollbar.set)
		self.code.pack(side=LEFT, expand=YES, fill=BOTH, padx=3, pady=3)
		self.scrollbar.config(command = self.code.yview)

		

	def load_file(self):
		fname = askopenfilename()
		time.sleep (3)
		if fname:
			thread1 = threading.Thread(target = self.buildGcode, args=(fname,))
			thread1.setDaemon(True)
			thread1.start()
			return 

	def buildGcode(self, fname):
		print(fname)
		self.code.delete(0.0, END)
		self.prepareTrayLabel['text'] = 'prepareTrayProgress: %%%d'%(0)
		self.generateGcodeLabel['text'] = 'generateGcodeProgress: %%%d'%(0)
		self.update_idletasks()

		file_id = uploadFile(fname)
		uuid = importMesh(file_id)
		uuid = importMeshResponse(uuid)
		uuid = transformMesh(uuid, self.getTransform())
		mesh_id = uuid
		uuid = analyzeMesh(mesh_id)
		if uuid == '':
			print('analyze mesh finished with no problem')
		elif uuid != 'timeout':
			uuid = reqairMesh(uuid)
		uuid = createTray(self.printer_id_e.get(), self.profile_e.get(), [mesh_id])
		uuid = createTrayResponse(uuid)
		tray_id = uuid
		uuid = prepareTray(tray_id)
		for i in range(60):
			progress = prepareTrayProgress(uuid)
			self.prepareTrayLabel['text'] = 'prepareTrayProgress: %%%d'%(progress*100)
			if progress == 1:
				break
			else:
				time.sleep(1)
		uuid = prepareTrayResponse(uuid)
		uuid = generateGcode(uuid)

		for i in range(60):
			progress = generateGcodeProgress(uuid)
			self.generateGcodeLabel['text'] = 'generateGcodeProgress: %%%d'%(progress*100)
			if progress == 1:
				break
			else:
				time.sleep(1)
		uuid = generateGcodeResponse(uuid)
		# downloadGcode(uuid, "/Users/lisper/test.gcode")
		self.gcode = getGcode(uuid)
		self.code.insert(END, self.gcode)
		return

	def save_file(self):
		fname = asksaveasfilename()
		if fname:
			print('fname : ' + fname)
			with open(fname, 'w') as f:
				f.write(str(self.gcode))
				print('file write sucess' + ' "' + fname + '"')
			return
	def getTransform(self):
		for i in range(3):
			for j in range(4):
				# print(self.e[i*4+j].get())
				self.transformData[i][j] = float(self.e[i*4+j].get())
				# print(self.transformData[i][j])
		return self.transformData

if __name__ == "__main__":
	MyFrame().mainloop()

