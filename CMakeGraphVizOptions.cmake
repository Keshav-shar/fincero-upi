# Read by `cmake --graphviz`. External libraries stay in the graph so that
# check_boundaries.py can catch core linking anything outside core.
set(GRAPHVIZ_EXTERNAL_LIBS TRUE)
set(GRAPHVIZ_INTERFACE_LIBS TRUE)
set(GRAPHVIZ_GENERATE_PER_TARGET FALSE)
set(GRAPHVIZ_GENERATE_DEPENDERS FALSE)
