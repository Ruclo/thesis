#!/bin/bash
set -e

# Run all 5 experiments
cd "$(dirname "$0")"

echo "Running 5 experiments with pyright self-healing..."

for i in {1..5}; do
    echo ""
    echo "======================================"
    echo "EXPERIMENT $i: Running with STP stps/${i}.md"
    echo "======================================"

    ./run_experiment.sh "../stps/${i}.md" "experiment_${i}"

    echo "Experiment $i complete!"
    echo ""
done

echo "All experiments complete!"
echo "Results in v1/experiment_1 through v1/experiment_5"
