#!/bin/bash
set -e

# Run all 5 experiments
cd "$(dirname "$0")"

echo "Running 5 experiments with 5-phase self-healing pipeline..."
echo "Model: ${MODEL:-opus4.6}"

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
echo "Results in ${MODEL:-opus4.6}/experiment_1 through ${MODEL:-opus4.6}/experiment_5"
