#!/usr/bin/env python3
import sys
import tomllib

from jinja2 import Template


def load_pyproject(path):
    with open(path, 'rb') as f:
        return  tomllib.load(f)


def process(path, **kwargs):
    with open(path, 'r') as f:
        tmpl = Template(f.read())

    base = kwargs['tool']['poetry']
    author_name, author_email = get_author(base['authors'])

    data = {
        'name': base['name'],
        'version': base['version'],
        'description': base['description'],
        'license':  base['license'],
        'requires': [parse_dep(k, v) for k, v in base['dependencies'].items() if k != 'python'],
        'console_scripts': [f'{k}={v}' for k, v in base['scripts'].items()],
        'packages': [p['include'] for p in base['packages']],
        'package_dir': {'': 'src'},
        'author_name': author_name,
        'author_email': author_email,
        'url': 'https://github.com/odra/bullgon',
    }

    return tmpl.render(**data)


def get_author(data):
    name, email = data[0].split(' ')

    return name, email.replace('<', '').replace('>', '')


def parse_dep(name, version):
    m = version[0]
    v = version[1:]
    major, minor, patch = v.split('.')

    if m == '~':
        ver_max = f'{major}.{int(minor) + 1}.0'
    elif m == '^':
        ver_max = f'{int(major) + 1}.0.0'
    else:
        return f'{name}={v}'

    return f'{name}>={v},<={ver_max}'


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else 'pyproject.toml'
    dest = sys.argv[2] if len(sys.argv) > 2 else 'setup.py'

    data = load_pyproject(src)
    content = process('hack/setup.py.j2', **data)

    with open(dest, 'w+') as f:
        f.write(content)


if __name__ == '__main__':
    main()
