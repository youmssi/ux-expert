#!/usr/bin/env bash
# Run every eval with and without the skill, each in a clean, isolated
# workspace, then grade the outputs and write a benchmark.
#
#   evals/run.sh [iteration-name]        e.g. evals/run.sh iteration-1
#
# Costs model tokens: one full agent session per eval and configuration
# (6 sessions per iteration). Uses Claude Code in headless mode; to use another
# agent, change run_agent(). Requires python3 with scripts/requirements.txt.
set -euo pipefail

ITERATION="${1:-iteration-1}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/evals-workspace/$ITERATION"

command -v claude >/dev/null || { echo "claude CLI not found; adapt run_agent() to your agent" >&2; exit 1; }

# run_agent <workdir> <prompt> <report-file>: the agent may only read files.
run_agent() {
  (cd "$1" && claude -p "$2" --output-format json --allowedTools "Read,Grep,Glob,Skill") \
    | python3 -c 'import json, sys; print(json.load(sys.stdin)["result"])' > "$3"
}

eval_ids=$(python3 -c "import json; print(' '.join(e['id'] for e in json.load(open('$ROOT/evals/evals.json'))['evals']))")

for id in $eval_ids; do
  prompt=$(python3 -c "import json; print(next(e['prompt'] for e in json.load(open('$ROOT/evals/evals.json'))['evals'] if e['id'] == '$id'))")
  for config in with_skill without_skill; do
    work=$(mktemp -d)
    mkdir -p "$work/evals"
    cp -r "$ROOT/evals/fixtures" "$work/evals/"
    find "$work/evals/fixtures" -name answers.yaml -delete  # the agent never sees the answer key
    if [ "$config" = with_skill ]; then
      mkdir -p "$work/.claude/skills"
      cp -r "$ROOT/skills/ux-expert" "$work/.claude/skills/"
    fi
    dest="$OUT/$id/$config"
    mkdir -p "$dest/outputs"
    start=$(date +%s)
    run_agent "$work" "$prompt" "$dest/outputs/report.md"
    echo "{\"duration_seconds\": $(( $(date +%s) - start ))}" > "$dest/timing.json"
    python3 "$ROOT/evals/grade.py" "$id" "$dest/outputs/report.md" --out "$dest/grading.json" > /dev/null
    echo "$id / $config: $(python3 -c "import json; print(json.load(open('$dest/grading.json'))['summary'])")"
    rm -rf "$work"
  done
done

python3 "$ROOT/evals/grade.py" --benchmark "$OUT" > /dev/null
echo "benchmark: $OUT/benchmark.json"
