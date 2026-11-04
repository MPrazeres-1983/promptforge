"""Missing or failed evaluators must not be treated as a successful run."""
from unittest.mock import Mock

import pytest
from promptforge.core.pipeline import EvalPipeline
from promptforge.core.run_config import EvaluatorConfig


def _pipeline_with_evaluator(evaluator):
    pipeline = object.__new__(EvalPipeline)
    pipeline.rc = Mock(evaluators=[evaluator])
    pipeline.console = Mock()
    pipeline.ps = Mock()
    return pipeline


def test_unknown_heuristic_fails_closed():
    p = _pipeline_with_evaluator(EvaluatorConfig(type="heuristic", name="does_not_exist"))
    with pytest.raises(ValueError, match="Unknown heuristic"):
        p._evaluate(Mock(expected={}), "{}", {}, "")


def test_missing_judge_rubric_fails_closed():
    p = _pipeline_with_evaluator(EvaluatorConfig(type="judge", name="quality"))
    with pytest.raises(RuntimeError, match="Judge evaluator"):
        p._evaluate(Mock(expected={}), "{}", {}, "")


def test_unknown_evaluator_type_fails_closed():
    p = _pipeline_with_evaluator(EvaluatorConfig(type="unknown", name="quality"))
    with pytest.raises(ValueError, match="Unknown evaluator type"):
        p._evaluate(Mock(expected={}), "{}", {}, "")
