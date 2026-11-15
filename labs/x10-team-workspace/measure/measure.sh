mkdir -p ~/x10/runs
export CLAUDE_CONFIG_DIR=~/x10/cfg CLAUDE_CODE_DISABLE_AUTO_MEMORY=1
MODEL=sonnet   # same model in every run

question() {
  case $1 in
    1) echo 'Where is the repo web-shop on disk, and which git remote does it have? Answer on one line.' ;;
    2) echo 'How are the tests run in orders-api? Answer with the command.' ;;
    3) echo 'Which rule applies to personal ID numbers in logs? Answer on one line.' ;;
  esac
}

run() {  # $1 arm (A|B), $2 directory, $3 question (1-3), $4 run (1-2)
  (cd "$2" && claude -p "$(question "$3")" --output-format stream-json --verbose \
    --tools "Read,Grep,Glob" --allowedTools "Read,Grep,Glob" \
    --settings ~/x10/measure-settings.json --model "$MODEL" \
    --no-session-persistence --max-turns 25 --max-budget-usd 2) \
    > ~/x10/runs/"$1"-q"$3"-r"$4".jsonl
}

for r in 1 2; do for q in 1 2 3; do run A ~/team-home "$q" "$r"; run B ~/work "$q" "$r"; done; done
