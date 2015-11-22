# Run this with this command line:
# $ python expandTemplate.py -c Customer.yaml -t EntityClass.jinja

import yaml,sys,jinja2

def getArgs():
    classDefFile = sys.argv[1]
    templateFile = sys.argv[2]
    outfile = sys.argv[3]
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