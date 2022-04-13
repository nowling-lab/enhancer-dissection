from setuptools import setup

setup(
    name='Fasta Highlighter',
    version='0.1',
    description='Applies fimo data onto a sequence file to visulize data',
    url='https://github.com/nowling-lab/enhancer-dissection',
    author='John Peters',
    author_email='John.Geraldo.Peters@gmail.com',
    license='Apache-2.0',
    packages=['clustal_highlighter'],
    zip_safe=False,
    python_requires=">=3.8",
    scripts=["bin/fasta_highlighter"],
    install_requires=['pandas>=1.3.4']
)