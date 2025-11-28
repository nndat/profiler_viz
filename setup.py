from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="profiler-viz",
    version="0.1.0",
    author="datnn",
    author_email="nguyenngocdat90@gmail.com",
    description="A beautiful Python profiler with interactive HTML visualization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nndat/profiler_viz",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        # No external dependencies required
    ],
    package_data={
        "profiler_viz": ["profile_template.html"],
    },
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "profiler-viz=profiler_viz.viewer:main",
        ],
    },
)
