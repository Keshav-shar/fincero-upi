find_package(Drogon CONFIG REQUIRED)
find_package(jsoncons CONFIG REQUIRED)
find_package(spdlog CONFIG REQUIRED)
find_package(unofficial-sodium CONFIG REQUIRED)

add_subdirectory(platform)

# Modules link only what they need, not all of fincero_core, so that a module with no
# business reaching the RNG cannot do so (Rule 7, cmake/check_boundaries.py).
add_subdirectory(modules/identity)
add_subdirectory(modules/upi_gateway)
add_subdirectory(modules/ledger_inr)
add_subdirectory(modules/ledger_cero)
add_subdirectory(modules/economy)
add_subdirectory(modules/market)
add_subdirectory(modules/assistant)
add_subdirectory(modules/notifications)

add_subdirectory(app)
