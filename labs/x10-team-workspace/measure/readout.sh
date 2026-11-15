printf 'run\tresult\test_list_usd\tturns\tseconds\tfiles_read\tgrep_glob_calls\tread_outside_catalog\n'
for f in ~/x10/runs/*.jsonl; do jq -s -r --arg run "$(basename "$f" .jsonl)" '
  (map(select(.type=="result"))[0]) as $r
  | [.[] | select(.type=="assistant") | .message.content[]? | select(.type=="tool_use")] as $t
  | [ $run, $r.subtype, $r.total_cost_usd, $r.num_turns, ($r.duration_ms/1000),
      ([$t[] | select(.name=="Read") | .input.file_path] | unique | length),
      ([$t[] | select(.name=="Grep" or .name=="Glob")] | length),
      ([$t[] | select(.name=="Read") | .input.file_path | select(contains("/catalog/") | not)] | length)
    ] | @tsv' "$f"; done
