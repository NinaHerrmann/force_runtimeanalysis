# force_runtimeanalysis

Document different settings with different runtimes.
Folders are named after the commit used in https://github.com/NinaHerrmann/force/ so they can be reproduced. Those are structured in baseline and opt to increase the readability. Reevaluate if this is nice.

Jobs are started with
`taskset -c 16-31 ./bin/force-level2 $PRMFILE` and `PAIRS=("16 1" "8 2" "4 4")` to get an idea if the changed code affects settings differently (of course this needs to be tested more extensive in the future).
