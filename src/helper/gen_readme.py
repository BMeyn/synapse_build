import jinja2
import yaml
import argparse


def generate_readme_jinja2(config_path, readme_template_path, output_file_path):
    """ generate_readme_jinja2 Module """

    # read parm_dict from yaml
    with open(config_path, 'r') as stream:
        parm_dict = yaml.full_load(stream)

    # read jinja2 template
    with open(readme_template_path, 'r') as stream:
        template = jinja2.Template(stream.read())

    # render jinja2 template
    readme_content = template.render(parm_dict)

    # save readme to files
    with open(output_file_path, "w") as f:
        f.write(readme_content)


# run generate_readme_jinja2 when script in run mode
# prase argument from command line
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate README.md from template')
    parser.add_argument('--config', help='config file path', required=True)
    parser.add_argument(
        '--template', help='readme template file path', required=True)
    parser.add_argument('--output', help='output file path', required=True)
    args = parser.parse_args()
    generate_readme_jinja2(args.config, args.template, args.output)
