import os
import sys
import platform

from setuptools import setup
from setuptools.command.install import install

MODULE_DIR = "csvsql"

def setup_module():
  classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Intended Audience :: System Administrators",
    "License :: OSI Approved",
    "Topic :: Database",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
  ]
  if is_linux(): 
    classifiers.append("Operating System :: POSIX")
    classifiers.append("Programming Language :: Python :: 3.7")
    python_requires = ">=3.7, <4"
  if is_mac():
    classifiers.append("Operating System :: MacOS")
    python_requires = ">=3.8, <4"

  cmdclass = { 'install': PostInstallCommand }

  setup(
    name = "csv-connector",
    version = "1.0",
    author = "MACDEV",
    author_email = "support@softtechcom.com",
    description = "CSV SQLAlchemy",
    python_requires = python_requires,
    url = "www.softtechcom.com",
    packages = [ MODULE_DIR ],
    package_data = { MODULE_DIR: ['*','*/*','*/*/*'] },
    classifiers = classifiers,
    cmdclass = cmdclass,
    entry_points = {
      "sqlalchemy.dialects": [
        "csv = csvsql.sqlalchemy_csv.dialect:CSVDBSDialect",
        "cdata_csv = csvsql.sqlalchemy_csv.dialect:CSVDBSDialect"
      ]
    },
  )

def is_mac():
  return platform.system().lower() == "darwin"

def is_linux():
  return platform.system().lower() == "linux"

def getArch():
  return platform.machine()

def getPythonVersion():
  return "py" + str(sys.version_info.major) + str(sys.version_info.minor)

class PostInstallCommand(install):
  def run(self):
    install.run(self)
    local_path = os.path.join(self.install_usersite, MODULE_DIR)
    base_path = os.path.join(self.install_base, "lib", "python" + self.config_vars["py_version_short"], "site-packages", MODULE_DIR)
    arch = getArch()
    os.system("./" + MODULE_DIR + "/csvrtutil.sh -b " + base_path + " -l " + local_path + " -a " + arch)
    operating_system = platform.system().lower()
    python_version = getPythonVersion()
    os.system("./" + MODULE_DIR + "/csvcleanup.sh -p " + base_path + " -o " + operating_system + " -v " + python_version)

if __name__ == "__main__":
  setup_module()