# Run this with this command line:
# $ python expandTemplate.py -c Customer.yaml -t EntityClass.jinja

import yaml,json,sys,jinja2,getopt

classDefFile = ""
templateFile = ""

options, remainder = getopt.getopt(sys.argv[1:], 'c:t:', ['classDefFile=',
                                                         'templateFile'
                                                         ])
for opt, arg in options:
    if opt in ('-c', '--classdeffile'):
        classDefFile = arg
    elif opt in ('-t', '--templatefile'):
        templateFile = arg


templateLoader = jinja2.FileSystemLoader(searchpath=".")
templateEnv = jinja2.Environment(loader=templateLoader, lstrip_blocks=True, trim_blocks=True)
template = templateEnv.get_template(templateFile)

with open(classDefFile, 'r') as f:
    config = yaml.load(f)
    outfileName = (config['class']['name'] + ".vr").lower()
    outputText = template.render(config)

    with open(outfileName, 'w') as outfile:
        outfile.write(outputText)