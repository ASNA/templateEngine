import yaml,json,sys,jinja2,getopt


classDefFile = ""
templateFile = ""

options, remainder = getopt.getopt(sys.argv[1:], 'c:t', ['classdeffile=',
                                                         'templatefile'
                                                         ])
for opt, arg in options:
    if opt in ('-c', '--classdeffile'):
        classDefFile = arg
    elif opt in ('-t', '--templatefile'):
        templateFile = arg

templateLoader = jinja2.FileSystemLoader(searchpath=".")
templateEnv = jinja2.Environment(loader=templateLoader, lstrip_blocks=True, trim_blocks=True)
TEMPLATE_FILE = "ClassWithGetterSetters.jinja"
template = templateEnv.get_template(TEMPLATE_FILE)

with open('fields.yaml', 'r') as f:
    config = yaml.load(f)
    outfileName = config['class']['name'] + ".vr"
    outputText = template.render(config)

    with open(outfileName, 'w') as outfile:
        outfile.write(outputText)