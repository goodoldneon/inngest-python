from setuptools import setup, find_packages

with open('README.md') as f:
  long_description = f.read()

setup(
  name="inngest",
  version="0.0.1",
  description="Inngest Python SDK",
  author="Inngest, inc.",
  author_email="eng@inngest.com",
  url="https://github.com/inngest/inngest-python/",
  keywords=["inngest"],
  install_requires=[
  ],
  extras_require={
    ':python_version<"3.0"': [
      "requests[security] >= 2.0.0",
    ],
    ':python_version>="3.0"': [
      "requests >= 2.0.0"
    ],
  },
  packages=find_packages(exclude=['tests', 'tests.*']),
  include_package_data=True,
  classifiers=[
    "Intended Audience :: Developers",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
  ],
  long_description=long_description,
  long_description_content_type='text/markdown'
)
