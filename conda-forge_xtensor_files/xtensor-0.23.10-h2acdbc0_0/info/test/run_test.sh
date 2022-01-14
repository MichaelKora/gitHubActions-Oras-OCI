

set -ex



test -d ${PREFIX}/include/xtensor
test -f ${PREFIX}/include/xtensor/xarray.hpp
test -f ${PREFIX}/lib/cmake/xtensor/xtensorConfig.cmake
test -f ${PREFIX}/lib/cmake/xtensor/xtensorConfigVersion.cmake
exit 0
