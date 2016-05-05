import yaml,sys,jinja2,getopt,os.path

map = [{"name": "owner", "column": "D", "nullable": True},
       {"name": "subject", "column": "E", "nullable": False}]


for m in map:
    print(m['name'])
    print(m['column'])
    print(m['nullable'])
