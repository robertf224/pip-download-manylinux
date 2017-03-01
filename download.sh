#!/bin/bash

# Pick python version based on environment variables.
PYBIN="/opt/python/${PYTHON_TAG}-${ABI_TAG}/bin"

# Download packages.
"${PYBIN}/pip" download -r /io/temp/requirements.txt -d /io/temp/downloads

# Move .whls to final landing place, they don't need to be compiled.
mv /io/temp/downloads/*.whl /io/packages/

# Compile each source distribution.
for source_distribution in /io/temp/downloads/*; do
    "${PYBIN}/pip" wheel "$source_distribution" -w /io/temp/intermediate-wheels
done

# Possibly repair each built wheel and place into final landing place.
for intermediate_wheel in /io/temp/intermediate-wheels/*.whl; do
	if [[ $intermediate_wheel == *linux_x86_64.whl ]]; then
  		auditwheel repair "$intermediate_wheel" -w /io/packages
  	else
  		mv $intermediate_wheel /io/packages
	fi
done



