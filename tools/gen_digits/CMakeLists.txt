# Offline digit generator. The only place GMP and MPFR are allowed.
find_package(PkgConfig REQUIRED)
pkg_check_modules(gmp REQUIRED IMPORTED_TARGET gmp)
pkg_check_modules(mpfr REQUIRED IMPORTED_TARGET mpfr)

fincero_add_executable(fincero_gen_digits
    SOURCES main.cpp
    DEPS PkgConfig::mpfr PkgConfig::gmp)
