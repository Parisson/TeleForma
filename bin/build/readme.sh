#!/bin/bash

cd "$(dirname "$0")"/../../

cat doc/src/overview.rst doc/src/architecture.rst doc/src/install.rst doc/src/development.rst doc/src/maintenance.rst doc/src/copyright.rst doc/src/license.rst > README.rst

echo "Build finished. The README.rst file is up to date."
