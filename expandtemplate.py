## expandtemplate.py
##
## NAME
##     expandtemplate.py - expand a template into a file.
##
## DESCRIPTION
##     Expand a template into a text file.##
##
##     -h, --help
##         Show help
##
##     Required arguments are:
##
##     -d, --deffile
##         The YAML definition file describing data to be used in the template.
##
##     -t, --templatefile
##         The template file
##
##     -o, --outfile
##         The outfile
##
## EXAMPLE
##     python expandtemplate.py -d def/customer.yaml -t tpl/EntityClass.jinja -o Customer.vr
##
# For Windows install
#    pip install PyYAML
#    pip install jinja2

import yaml,sys,jinja2,getopt,os.path

def usage():
    with open('expandtemplate.py', 'r') as f:
        for line in f:
            if (line.startswith('##')):
                sys.stdout.write(line[2:])

def getArgs():
    classDefFile = ""
    templateFile = ""
    outfile = ""
    ##global classDefFile, templateFile
    try:
        options, remainder = getopt.getopt(sys.argv[1:],
            'd:t:o:h', ['deffile=','templatefile=','outfile=','help' ])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        sys.exit(2)

    for opt, arg in options:
        if opt in ('-h', '--help'):
            usage()
            sys.exit()
        elif opt in ('-d', '--deffile'):
            classDefFile = arg
            if ( not os.path.isfile(classDefFile)):
                print( 'Class definition file not found: ' + classDefFile)
                sys.exit(2)
        elif opt in ('-t', '--templatefile'):
            templateFile = arg
            if ( not os.path.isfile(templateFile)):
                print( 'template file not found: ' + templateFile)
                sys.exit(2)
        elif opt in ('-o', '--outfile'):
            outfile = arg

    if (templateFile == ''):
        print("'templatefile' argument must be defined.")
        usage()
        sys.exit(2)

    if (classDefFile == ''):
        print("'deffile' argument must be defined.")
        usage()
        sys.exit(2)

    if (outfile == ''):
        print("'outfile' argument must be defined.")
        usage()
        sys.exit(2)

    return classDefFile, templateFile, outfile

def loadTemplate(templateFile):
    templateLoader = jinja2.FileSystemLoader(searchpath=".")
    templateEnv = jinja2.Environment(loader=templateLoader, lstrip_blocks=True, trim_blocks=True)
    template = templateEnv.get_template(templateFile)
    return template

def writeFile(template, classDefFile, outfile):
    with open(classDefFile, 'r') as f:
        config = yaml.load(f)
        if (outfile == ''):
            outfile = (config['class']['name'] + ".vr").lower()

        outputText = template.render(config)

        with open(outfile, 'w') as outfile:
            outfile.write(outputText)

    return outfile

classDefFile, templateFile, outfile = getArgs()
template = loadTemplate(templateFile)
writeFile(template, classDefFile, outfile)