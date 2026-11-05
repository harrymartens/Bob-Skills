SKILLS := operating-discipline pptx docx pdf research
.PHONY: eval eval-% baseline-% trigger-% check-tools install test

## Run every skill eval through Bob (needs bob + BOB_API_KEY)
eval: $(addprefix eval-,$(SKILLS))
	@echo; echo "== results"; for s in $(SKILLS); do printf "%-22s %s\n" $$s "$$(cat evals/$$s/runs/LATEST 2>/dev/null || echo 'not run')"; done

eval-%:
	bash tools/run_eval.sh $*

## Same task with the skill disabled, for the before/after comparison
baseline-%:
	bash tools/run_eval.sh $* --no-skill

## Does Bob choose the skill from its description without being told?
trigger-%:
	bash tools/run_trigger_eval.sh $*

## Verify the checkers and helpers work on this machine without Bob (python-pptx, docx, pypdf, soffice)
test:
	bash tools/selftest.sh

## Copy skills and rules into ~/.bob (global) or ./.bob of a target project: make install TARGET=~/.bob
install:
	bash install.sh $(TARGET)

check-tools:
	@for t in python3 soffice pdftoppm markitdown curl bob; do printf "%-10s " $$t; command -v $$t >/dev/null && echo ok || echo MISSING; done
	@python3 -c "import pptx, docx, pypdf, PIL; print('python deps ok')"
