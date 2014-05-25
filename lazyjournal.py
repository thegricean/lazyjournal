#!/usr/bin/python

import csv
from datetime import datetime
import shutil
from Tkinter import *
import tkSimpleDialog
from ttk import Combobox

################################
# the main application class #
################################
class LazyJournal(Frame):
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.loadPrevResults()
		self.loadQuestions()
		self.loadDefaultAnswers()
		self.createScrollbar()
		self.questionmenus = []
		self.createJournalEntries()
		self.createButtons()


	def createScrollbar(self):
		self.canvas = Canvas(self.master, borderwidth=0)
		self.frame = Frame(self.canvas)
		self.scrollbar = Scrollbar(self.master, orient="vertical", command=self.canvas.yview)
		self.canvas.configure(yscrollcommand=self.scrollbar.set)
		self.scrollbar.pack(side="right", fill="y")
		self.canvas.pack(side="left", fill="both", expand=True)
		self.canvas.create_window((4,4), window=self.frame, anchor="nw", 
                                  tags="self.frame")
		self.frame.bind("<Configure>", self.OnFrameConfigure)
		
	def OnFrameConfigure(self, event):
		self.canvas.configure(scrollregion=self.canvas.bbox(ALL),width=400,height=500)
	
	def loadDefaultAnswers(self):
		# load default answers to questions
		self.defaultanswers = {}
		for qu in [q['ID'] for q in self.questions]:
			self.defaultanswers[qu] = ""
		try:
			dfile = open("defaults.csv")
			for da in [sp.split("\t") for sp in [l.rstrip() for l in dfile.readlines()[1:]]]:
				self.defaultanswers[da[0]] = da[1]
			shutil.copyfile("defaults.csv",".defaults.backup")
			dfile.close()
		except IOError:
			print "no default answers found"
	
	def loadPrevResults(self):
		# load previous journal entries
		try:
			rfile = open("result.csv")
			reader = csv.DictReader(rfile,delimiter="\t",quotechar='\"')
			self.prevresults = list(reader)
			shutil.copyfile("result.csv", ".result.backup")
			rfile.close()			
		except IOError:
			self.prevresults = []
			print "no previous journal entries found"

	def loadQuestions(self):
		# load questions
		try:
			qfile = open("questions.txt",'r')
			reader = csv.DictReader(qfile,delimiter="\t",quotechar='\"')
			self.questions = list(reader)
			shutil.copyfile("questions.txt", ".questions.backup")
			qfile.close()
		except IOError:
			self.questions = []
			print "no questions found"

	def createJournalEntries(self):
		# iterate through questions
		for i,q in enumerate(self.questions):
			fname = "library/"+q['ID']+".txt"
			answerfile = open(fname)
			answers = [l.rstrip() for l in answerfile.readlines()]	
			self.questionmenus.append({'ID':q['ID'],'JournalEntry':JournalEntry(self.frame, q['Question'], i, self.defaultanswers[q['ID']], *answers),'Answers':answers})
			answerfile.close()
		
		# number of questions for positioning purposes
		self.nq = len(self.questions) + 1

	def createButtons(self):
		try:
			self.buttonframe.destroy()
		except AttributeError:
			pass
		# a bunch of buttons	
#		self.buttonframe = Frame(self.master)
		self.buttonframe = Frame(self.frame)
		self.buttonframe.grid(row=self.nq, column=0, columnspan=3) 
		        	
		# button to record responses	
		self.okbutton = Button(self.buttonframe, text="OK", command= lambda:ok(self.questionmenus, self.prevresults)).grid(row=self.nq, column=0)
		
		# button to close without recording responses
		self.cancelbutton = Button(self.buttonframe, text="Cancel", command=self.master.quit).grid(row=self.nq, column=1)
		
		# button to add a question manually
		self.qbutton = Button(self.buttonframe, text="Add question", command= lambda:self.addQuestion(self.questionmenus,self.frame)).grid(row=self.nq, column=2)

		# button to add a default value to a question (or change the default value if it exists)
		self.defaultbutton = Button(self.buttonframe, text="Add default", command= lambda:self.addDefault(self.questionmenus,self.defaultanswers,self.frame)).grid(row=self.nq, column=3)


	# add/change default value for a question
	def addDefault(self, qm, danswers, parent):
		newda = NewDefault(parent, qm)
		#if newda.value[0] in danswers.keys():
		danswers[newda.value[0]] = newda.value[1]
		self.writeDefaultsToFile(danswers)

	# add a question	
	def addQuestion(self, qm, parent):
		newquestion = NewQuestion(parent, qm)
		self.nq = self.nq + 1
		print newquestion.value
		self.questionmenus.append({'ID':newquestion.value[2], 'JournalEntry':JournalEntry(self.frame,newquestion.value[0], self.nq - 1, newquestion.value[1], *[newquestion.value[1]])})
		self.createNewAnswerFile(newquestion.value[2],newquestion.value[1])
		self.addNewQuestionToFile([newquestion.value[2],newquestion.value[0]])
		self.createButtons()

	def writeDefaultsToFile(self,vals):
		defaultfile = open("defaults.csv","w")
		defaultfile.write("ID\tdefaultanswer\n")
		defaultfile.write("\n".join(["\t".join([v,vals[v]]) for v in vals.keys() if len(vals[v]) > 0]))
		defaultfile.close()
		
	def addNewQuestionToFile(self,vals):
		questionfile = open("questions.txt","a")
		questionfile.write("\n"+"\t".join(vals))
		questionfile.close()

	def createNewAnswerFile(self,idname, answer):
		fname = "library/"+idname+".txt"
		answerfile = open(fname,'w')
		answerfile.write(answer)
		answerfile.close()
		

################################
# the journal entry class #
################################
class JournalEntry(LabelFrame):
	def __init__(self, parent, question, i, defaultanswer, *options):
		LabelFrame.__init__(self, parent, text=question, padx=5, pady=5)
		self.var = StringVar(parent)
		try:
			if defaultanswer in options:
				options = tuple(x for x in options if x != defaultanswer)
			options = (defaultanswer,) + options		
			self.var.set(options[0])
		except IndexError:
			self.var.set("")
		self.om = Combobox(self, textvariable=self.var)
		self.om['values'] = options
		self.om.pack(padx=5,pady=5, side="left")
		self.grid(row=i,column=0,columnspan=3, sticky=W, pady=10)

#############################
# new question dialog class #
#############################
class NewQuestion():
	def __init__(self, parent, qm):
		self.qm = qm
		keywords = [k['ID'] for k in self.qm]
		self.parent = parent
		self.value = []
		self.value.append(tkSimpleDialog.askstring("","Enter a new question."))
		self.value.append(tkSimpleDialog.askstring("", self.value[0]))
		newkeyword = tkSimpleDialog.askstring("", "Enter a new keyword to identify this question.")
		while newkeyword in keywords:
			newkeyword = tkSimpleDialog.askstring("", "The keyword "+newkeyword+" is already in use. Please enter a new keyword to identify this question.")
			
		self.value.append(newkeyword)

###################################
# new default answer dialog class #
###################################
class NewDefault():
	# this currently asks for the question ID and a default answer. This means you need to know the question ID (all question IDs are printed to the terminal)
	# this is of course not the ideal way to do it - you want to have a table where you can select the question and add an answer (maybe even choose the answer from a dropdown menu of already available answers)
	def __init__(self, parent, qm):
		self.qm = qm
		keywords = [k['ID'] for k in self.qm]
		self.parent = parent
		self.value = []
		print keywords		
		self.value.append(tkSimpleDialog.askstring("","Enter the question ID for which you would like to enter a default response (see terminal for question IDs)."))
		self.value.append(tkSimpleDialog.askstring("", "Enter the default response to the question: %s"%self.value[0]))		



# write journal entry to file
def ok(qm, previousresults):
	newresults = {q['ID']:q['JournalEntry'].var.get() for q in qm}
	newresults['datetime'] = datetime.isoformat(datetime.now())
	previousresults.append(newresults)
	print "adding new answers..."	
	for q in qm:
		aname = "library/"+q['ID']+".txt"
#		print aname
		answerfile = open(aname)
		answers = [l.rstrip() for l in answerfile.readlines()]
#		print answers
		if not q['JournalEntry'].var.get() in answers:
			answers.append(q['JournalEntry'].var.get())
			print answers
			answers.sort()		
			answerfile = open(aname,'w')
			answerfile.write("\n".join(answers))
			answerfile.close()
		else:
			print "no new answers"
	
	print "adding new questions..."
	if len(set(previousresults[0].keys())^set(newresults.keys())) > 0:
		newkeys = set(previousresults[0].keys())^set(newresults.keys())
		for n in newkeys:
			for p in previousresults[:-1]:
				p[n] = 'NA'
	else:
		print "no new questions"
	headers = previousresults[0].keys()
	outfile = open('result.csv','wb')
	w = csv.DictWriter(outfile,fieldnames=headers,delimiter="\t")
	w.writeheader()
	w.writerows(previousresults)
	outfile.close()
	root.quit()

		
################################################
# FIRE IT UP
################################################
root = Tk()
root.title("Lazy Journal")
root.grid()
app = LazyJournal(master=root)
app.mainloop()



