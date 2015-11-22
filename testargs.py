import sys, getopt

templateFilename = ""
outputFilename = ""

options, remainder = getopt.getopt(sys.argv[1:], 'o:t', ['outputfile=',
                                                         'templatefile'
                                                         ])
for opt, arg in options:
    if opt in ('-o', '--outputfile'):
        outputFilename = arg
    elif opt in ('-t', '--templatefile'):
        templateFileName = arg

print 'outputFilename    :', outputFilename
print 'templateFilename  :', templateFilename