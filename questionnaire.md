# Week 2 verified agent questionnaire

Name / team:

Repository URL or source ZIP: https://github.com/AimenFH/framework-agent-lab.git

Local model tag and preflight result: `qwen3:8b`, `LIVE PROBE PASSED`

Answer each in two to five clear sentences and refer to your four-minute video.
Scripted diagnostics support development; completion requires a live repair.

1. Which part of the Week 1 loop did LangGraph replace? Explain the nodes,
   message updates, routes, and what the 32-step limit guarantees.

   Answer: In Week 1 I wrote the while loop myself: call the model, run the tool
   it asked for, feed the result back. LangGraph replaces that loop with three
   nodes. `model` adds the system instruction and returns only the new
   `AIMessage`, `tools` (a `ToolNode`) returns a `ToolMessage` linked to each
   call, and `verify` decides the result. `MessagesState` appends every update to
   the history. `tools_condition` routes tool calls to `tools`, which always goes
   back to `model`, and routes a plain answer to `verify` and then END. You can
   see this in `build_agent`.

2. Which boundaries do the supplied tools enforce regardless of the model's
   request? Explain both denials and why a fixed test command still needs review.

   Answer: The tools check every path in Python, so the model can only read
   visible files inside `target-service`: no absolute paths, no `..`, no hidden
   folders, no symlinks, and nothing over 12,000 bytes. `edit_pricing` can only
   touch `orders/pricing.py`, and `run_tests` runs one fixed command, only after I
   type exactly `yes`. Reading `../HANDOUT.md` failed because the path leaves the
   service folder. Replacing `Decimal` with `float` failed because `Decimal`
   appears several times, so the tool can't know which one to change. The command
   is fixed, but running the tests still executes the code the model just wrote,
   with my permissions and no sandbox, so I read the diff before approving, as
   shown in the video.

3. How does your verification node distinguish a final response from verified
   completion? Explain failed/denied tests and an edit after a passing test.
   Identify one incomplete result you demonstrated.

   Answer: The model's final answer is just text, so my `verify` node ignores it
   and replays the `ToolMessage` results in order. A successful edit resets the
   test status. Each test run then replaces it: `exit_code=0` counts as a pass,
   and a failure, `DENIED` or `ERROR` clears it. So if the model edits the file
   after a passing test, that old pass no longer counts. The run is `verified`
   only if the last message is a real answer with no tool calls and the latest
   test result is a pass.

4. What evidence shows that the live model read, edited, and tested the service?
   State the model tag, your regression's expected business result and baseline
   failure, the final test result, and protected files you checked. What remains
   unverified?

   Answer: The video shows `qwen3:8b` calling `read_file` on the business rules,
   the acceptance tests and `orders/pricing.py`, then `edit_pricing` once and
   `run_tests`, each with its tool result printed underneath, and `git diff`
   shows exactly what the model changed. My regression prices 37.335 × 3 with an
   11% discount: discounted goods come to 99.69, so shipping is 5.00 and the total
   should be EUR 104.69. On the original code it failed with
   `Decimal('112.005') != Decimal('112.01')`. After the repair, the agent's test
   run returned `exit_code=0`, my own run passed all 10 tests, and the diff was
   empty for `validation.py`, `service.py`, `storage.py`, `test_acceptance.py`
   and `docs`. I haven't verified inputs the tests don't cover, whether another
   run of the model would also work, or safety without a sandbox.
