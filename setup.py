# First, we try to use setuptools. If it's not available locally,
# we fall back on ez_setup.
try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

long_description = ''

install_requires = []
with open('requirements.txt') as requirements_file:
    for line in requirements_file:
        line = line.strip()
        if len(line) == 0:
            continue
        if line[0] == '#':
            continue
        pinned_version = line.split()[0]
        install_requires.append(pinned_version)

setup(
    name='translator-modules',
    description='NCATS Translator Reasoner modules',
    packages=find_packages(),
    package_data={'ncats.translator.identifiers': ['*.txt']},
    url='https://github.com/ncats/translator-modules',
    download_url='https://github.com/ncats/translator-modules',
    entry_points={
        'console_scripts': [
            'identifier_resolver = ncats.translator.identifiers.resolver:main',
            'tissue_to_tissue_bicluster = ncats.translator.modules.anatomical_entity.anatomical_entity.tissue_to_tissue_bicluster:main',
            'tissue_to_gene_bicluster = ncats.translator.modules.anatomical_entity.gene.tissue_to_gene_bicluster:main',
            'chemical_to_gene_interaction = ncats.translator.modules.chemical_substance.gene.chemical_to_gene_interaction:main',
            'disease_associated_genes = ncats.translator.modules.disease.gene.disease_associated_genes:main',
            'disease_to_phenotype_bicluster = ncats.translator.modules.disease.phenotypic_feature.disease_to_phenotype_bicluster:main',
            'gene_to_tissue_bicluster = ncats.translator.modules.gene.anatomical_entity.gene_to_tissue_bicluster:main',
            'gene_to_cell_line_bicluster_DepMap = ncats.translator.modules.gene.cell_line.gene_to_cell_line_bicluster_DepMap:main',
            'gene_to_chemical_interaction = ncats.translator.modules.gene.chemical_substance.gene_to_chemical_interaction:main',
            'functional_similarity = ncats.translator.modules.gene.gene.functional_similarity:main',
            'phenotype_similarity = ncats.translator.modules.gene.gene.phenotype_similarity:main',
            'gene_interaction=modules.gene.gene.gene_interaction:main',
            'gene_to_gene_bicluster_RNAseqDB = ncats.translator.modules.gene.gene.gene_to_gene_bicluster_RNAseqDB:main',
            'gene_to_gene_bicluster_DepMap = ncats.translator.modules.gene.gene.gene_to_gene_bicluster_DepMap:main',
            'phenotype_to_disease_bicluster = ncats.translator.modules.phenotypic_feature.disease.phenotype_to_disease_bicluster:main',
        ]
    },
    long_description=long_description,
    install_requires=install_requires,
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-cov', 'mock'],
    license='Apache 2.0',
    zip_safe=False,
    author='James Eddy;Richard Bruskiewich',
    author_email='james.a.eddy@gmail.com; richard@starinformatics.com',
    version='0.3.3'
)