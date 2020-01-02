from setuptools import setup, find_packages

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    long_description = open('README.md').read()

# def install_deps():
#     default = open('requirements.txt', 'r').readlines()
#     new_pkgs = []
#     links = []
#     for resource in default:
#         if 'git+ssh' in resource or 'git+https' in resource:
#             pkg = resource.split('#')[0].replace('git+', '')
#             links.append(resource.strip())
#             pkgBase = pkg.split('/')[-1].replace('.git', '')
#             new_pkgs.append(pkgBase + '@ ' + pkg + '@master')
#             # new_pkgs.append(pkg.replace('egg=', '').rstrip())
#         else:
#             new_pkgs.append(resource.strip())
#     return new_pkgs, links

# pkgs, new_links = install_deps()

# print(pkgs)


setup(
    name = "geferon",
    version = "1.0.0",
    author = "Geferon",
    author_email = "geferon38@gmail.com",
    description = "A simple module to add extensibility to weblate",
    keywords = "weblate formats",
    packages=find_packages(),
    install_requires=[
        'pycountry',
        'chardet',
        'vdf @ https://github.com/geferon/vdf/tarball/master'
    ],
    long_description=long_description,
)