# Week 2 verified coding-agent lab

This lab replaces Week 1's controller with a live local Ollama model,
LangGraph tool routing, and an explicit verification decision. You use
four supplied scoped tools and implement response validation, model invocation,
graph construction, and verification.

Start with [HANDOUT.md](HANDOUT.md). Begin the lab by setting up Python 3.12,
installing the dependencies from `requirements-lock.txt`, downloading
`qwen3:8b`, and running `checks/probe_model.py`.
The model uses native calls, with reasoning disabled and bounded context,
generation, and timeouts. A scripted or manual repair does not complete the lab.

- `starter/agent.py`: supplied tools, model factory, CLI, and four TODO sections.
- `checks/probe_model.py`: local native-tool preflight before granting file tools.
- `checks/smoke.py`: read-only graph/state diagnostic.
- `checks/workflow.py`: harmless temporary-fixture write/test/verification checks.
- `target-service/`: defective service and nine original acceptance tests.
- `task.txt`: the repair task, configurable through `--task`.
- `questionnaire.md`: required answer template.
- `requirements.txt` / `requirements-lock.txt`: pinned framework dependencies.

Keep the agent outside the service. Independently author a regression before
running the live repair, then show ten passing tests and an empty protected-file
diff. Submit source, questionnaire, and one four-minute explanation video.

## My submission

### Environment
- macOS, Python 3.12.15 (Homebrew), Ollama 0.40.0
- Model: `qwen3:8b`, run locally with reasoning disabled and temperature 0
- Preflight: `python checks/probe_model.py --model qwen3:8b` printed `LIVE PROBE PASSED`

### Setup
```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-lock.txt
python -m pip check
ollama pull qwen3:8b
python checks/probe_model.py --model qwen3:8b
```

### Baseline and regression
With the original pricing, 9 tests ran: 5 failed and 4 passed.

My regression in `target-service/tests/test_student.py` prices one line of
EUR 37.335 × 3 with an 11% discount. The line total of 112.005 rounds half up to
112.01. The discount is 112.01 × 0.11 = 12.3211, rounded to 12.32, which leaves
99.69 of discounted goods. That is under 100.00, so shipping is EUR 5.00 and the
expected total is EUR 104.69.

Against the original pricing the test fails with
`Decimal('112.005') != Decimal('112.01')`. The original code also charges no
shipping and returns a total of 99.68.

### Diagnostics
```bash
python checks/smoke.py --agent starter/agent.py --root target-service
python checks/workflow.py --agent starter/agent.py
```
Both passed (`SMOKE PASSED`, `WORKFLOW PASSED`).

### Live repair
```bash
python starter/agent.py --root target-service --model qwen3:8b --task "$(cat task.txt)"
```
The model chose these steps:
1. `read_file` on docs/business-rules.md
2. `read_file` on tests/test_acceptance.py
3. `read_file` on orders/pricing.py
4. `edit_pricing`, replacing the whole file in one call
5. `run_tests`, which I approved with `yes` after reviewing the diff

The tests returned `exit_code=0` with 10 tests OK, and the run ended `VERIFIED`.
The new code rounds each line to cents with ROUND_HALF_UP, rounds the discount
amount, decides shipping from the discounted goods, and adds shipping after the
discount.

### Independent verification
```bash
cd target-service
git status --short
git diff -- orders/pricing.py
git diff --exit-code -- orders/validation.py orders/service.py orders/storage.py tests/test_acceptance.py docs
python -m unittest discover -s tests -v
```
Only `orders/pricing.py` (modified) and `tests/test_student.py` (new) changed.
The protected-file diff is empty, and all 10 tests passed.

### Incomplete result
On a copy of the original service, I answered `no` at the test approval. The tool
returned `DENIED` and the model replied without any passing test. Verification
reported `INCOMPLETE: latest test run did not pass: DENIED…` and the agent
exited with code 2.

### Limitations
- The tests only check the cases they contain, so other inputs are not proven correct.
- Running the tests executes model-edited Python with my user permissions, without an OS sandbox.
- A small local model can behave differently on another run, so one success does not show that every run succeeds.
- Approval depends on a person reviewing the diff before typing `yes`.
