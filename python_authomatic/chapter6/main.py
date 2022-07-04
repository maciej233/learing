from jinja2 import Environment, FileSystemLoader
import yaml

ENV = Environment(loader=FileSystemLoader('.'))

template = ENV.get_template("template.j2")


with open("data.yaml", 'r') as f:
    data = yaml.load(f)
    print(template.render(interface_list=data))

