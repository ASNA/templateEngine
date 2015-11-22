import yaml,json,sys,jinja2


templateLoader = jinja2.FileSystemLoader(searchpath=".")
templateEnv = jinja2.Environment(loader=templateLoader)
TEMPLATE_FILE = "example2.jinja"
template = templateEnv.get_template(TEMPLATE_FILE)

with open('fields.yaml', 'r') as f:
    config = yaml.load(f)
    print config
    #json.dump(config, sys.stdout, indent=4)
    #x = json.dumps(config)
    #print x
    # print x
    # fields = x['fields']
    # print fields
    # for f in x['fields']:
    #     print f['name']



    outputText = template.render(config)
    print outputText



    # with open('roger.json', 'w') as outfile:
    #     #json.dump(config, outfile)
    #     x = json.dumps(config)
    #     print x
    #     outputText = template.render(x)
    #     print outputText



    # fields = config['fields']
    # for field in fields:
    #     print field['name']








# stream = open("fields.yaml", "r")
# sections = yaml.load_all(stream)
# for section in sections:
#     for s in section.items():
#         print s
#         # if k=="fields":
#         #     for field in k:
#         #         print field
#         #print k, "->", v
#         #print "\n",