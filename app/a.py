import os, filecmp
from time import sleep
codes = {200:'success',404:'file not found',400:'error',408:'timeout'}

def compile(file,lang):
    if lang == 'java':
        class_file = file[:-4]+"class"
    elif lang == 'c':
        class_file = file[:-2]
    elif lang=='cpp':
        class_file = file[:-4]   
    if (os.path.isfile(class_file)):
        os.remove(class_file)
    if (os.path.isfile(file)):
        if lang == 'java':
            os.system('javac '+file)
        elif lang == 'c' or lang == 'cpp':
            os.system('g++ -o '+class_file+' '+file)
        if (os.path.isfile(class_file)):
            return 200
        else:
            return 400
    else:
        return 404

def run(file,input,timeout,lang,lan):
    if lang == 'java':
        cmd = 'java '+file
    elif lang=='c' or lang=='cpp':
        cmd = './'+file
    if lang == 'python':
        cmd = 'python '+file+".py"
    r = os.system(cmd+' < '+input+' > out.txt')
    if r==31744:
        os.remove('out.txt')
        return 408
    else:
        return 200
	  

def match(output):
    if os.path.isfile('out.txt') and os.path.isfile(output):
        b = filecmp.cmp('out.txt',output)
        #os.remove('out.txt')
        print output
        return b
    else:
        return 404

