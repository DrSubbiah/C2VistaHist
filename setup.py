from setuptools import setup, find_packages

setup(
    name             = "c2vistahist",
    version          = "0.1.0",
    author           = "Dr Subbiah",
    author_email     = "",
    description      = "Enriched Univariate Histogram — Cepheus AI Labs",
    url              = "https://github.com/DrSubbiah/C2VistaHist",
    packages         = find_packages(),
    install_requires = [
        "numpy",
        "pandas",
        "plotly",
        "scipy",
    ],
    python_requires  = ">=3.7",
)
