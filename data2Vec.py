import sys
import re
import pickle


def openfiles(inname,dumpname):
	dumpfile = open(dumpname,"w")
	with open(inname, 'r') as infile:
		arr = []
		num = 0
		for line in infile:
			if len(filter(None, re.split('[,(,), ]', line))) == 1:
				if len(arr)!=0:
					#print arr
					pickle.dump(arr,dumpfile)
					arr = []
					num += 1
			arr += map(float,filter(None, re.split('[,(,), ,\n]', line)))
	dumpfile.close()
	print "finish dumping %d files." % (num)

def loaddump(dumpname,outarr):
	dumpfile = open(dumpname,"r")
	while True:
		try:
			outarr.insert(0,pickle.load(dumpfile))
		except EOFError:
			break

def main(argv):
	for i in range(0,len(argv)-2):
		outarr = []
		openfiles(argv[i*2+1],argv[i*2+2])
		loaddump(argv[i*2+2],outarr)
		print "loading %d files." % (len(outarr))
	return

if __name__ == "__main__":
	if len(sys.argv) <= 2:
		print "usage:\n\t\tpython2.7 data2Vec.py #OfFiles InputFileName1 OutputFileName1 InputFileName2 OutputFileName2..."
		exit(1)
	main(sys.argv)