from setuptools import setup

setup(
    name='Fasta Highlighter',
    version='0.1',
    description='Applies fimo data onto a sequence file to visulize data',
    url='https://github.com/nowling-lab/enhancer-dissection',
    author='John Peters',
    author_email='John.Geraldo.Peters@gmail.com',
    license='Apache-2.0',
    packages=['clustal_highlighter', 'clustal_highlighter/modules', 'clustal_highlighter/modules/data_structures'],
    zip_safe=False,
    python_requires=">=3.8.10",
    scripts=[
        "bin/genome_highlighter",
        "bin/run_fimo_on_file",
        "bin/fasta_highlighter",
        "bin/run_vcf_tools_pi"
        ],
    install_requires=['pandas>=1.3.4', 'numpy>=1.22.3'],
    include_package_data=True,
)