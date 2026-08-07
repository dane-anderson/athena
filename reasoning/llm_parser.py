"""
Athena LLM Quant Request Parser

Uses a lightweight local LLM to interpret quantitative
research language that Athena's deterministic parser
cannot fully classify.

Core rules:

1. Deterministic parsing is authoritative.
2. Fields explicitly resolved by the deterministic
   parser may never be overwritten by the LLM.
3. Asset identity always remains deterministic.
4. The LLM may fill unresolved quantitative fields only
   when it provides evidence grounded in the user's words.
5. Invalid or unsupported LLM output is ignored.
6. If the LLM fails, Athena returns the deterministic
   baseline unchanged.
"""

import json
import re

from models.ollama_client import OllamaClient

from reasoning.athena_persona import ATHENA_QUANT_PERSONA
from reasoning.context_builder import build_research_context
from reasoning.parser import parse_quant_request as rule_based_parse
from reasoning.quant_request import QuantRequest


ALLOWED_TASKS = {
    "general_analysis",
    "risk_analysis",
    "simulation",
    "portfolio_analysis",
    "stress_test",
    "optimization",
}


ALLOWED_MODELS = {
    "historical",
    "gaussian",
    "student_t",
}


MODEL_ALIASES = {
    "historical": "historical",
    "historical simulation": "historical",
    "gaussian": "gaussian",
    "normal": "gaussian",
    "normal distribution": "gaussian",
    "student_t": "student_t",
    "student-t": "student_t",
    "student t": "student_t",
    "student's t": "student_t",
}


METRIC_ALIASES = {
    "var": "value_at_risk",
    "value at risk": "value_at_risk",
    "value_at_risk": "value_at_risk",

    "es": "expected_shortfall",
    "expected shortfall": "expected_shortfall",
    "expected_shortfall": "expected_shortfall",

    "vol": "volatility",
    "volatility": "volatility",

    "drawdown": "max_drawdown",
    "max drawdown": "max_drawdown",
    "maximum drawdown": "max_drawdown",
    "max_drawdown": "max_drawdown",

    "return": "returns",
    "returns": "returns",
}


class QuantLLMParser:

    def __init__(
        self,
        llm=None,
        model="qwen3:14b",
    ):
        self.llm = llm or OllamaClient()

        self.model = model

        self.current_message = ""

        self.last_analysis = {}

        self.last_warning = None


    def parse(self, message):
        """
        Parse a natural-language quantitative request.
        """

        self.current_message = message
        self.last_analysis = {}
        self.last_warning = None

        baseline = rule_based_parse(
            message
        )

        context = build_research_context(
            message
        )

        prompt = self._build_prompt(
            message,
            context,
            baseline,
        )

        try:

            response = self.llm.generate(
                prompt,
                model=self.model,
            )

            data = self._extract_json(
                response
            )

            self.last_analysis = data

            return self._build_request(
                data,
                baseline,
            )

        except Exception as error:

            self.last_warning = str(
                error
            )

            return baseline


    def _build_prompt(
        self,
        message,
        context,
        baseline,
    ):
        """
        Build Athena's structured interpretation prompt.
        """

        resolved = sorted(
            baseline.resolved_fields
        )

        return f"""
{ATHENA_QUANT_PERSONA}

RESEARCH CONTEXT:

{context}

USER REQUEST:

{message}

DETERMINISTICALLY RESOLVED FIELDS:

{resolved}

Athena's deterministic parser has already resolved
the fields listed above.

You MUST NOT reinterpret or replace those fields.

Your job is only to identify missing meaning or
parameters that are clearly supported by the user's
actual words.

Return ONLY valid JSON using this schema:

{{
    "task": null,
    "assets": [],
    "scenario": null,
    "lookback_days": null,
    "time_horizon_days": null,
    "simulations": null,
    "confidence_levels": [],
    "models": [],
    "metrics": [],
    "compare_assets": null,
    "evidence": {{
        "task": null,
        "scenario": null,
        "lookback_days": null,
        "time_horizon_days": null,
        "simulations": null,
        "confidence_levels": null,
        "models": null,
        "metrics": null,
        "compare_assets": null
    }}
}}

EVIDENCE RULE:

For every quantitative field you infer, place the exact
supporting words from USER REQUEST into that field's
evidence value.

Example:

USER REQUEST:
"Show me Nvidia's one-in-a-hundred left-tail loss."

Valid interpretation:

{{
    "task": "risk_analysis",
    "confidence_levels": [0.99],
    "evidence": {{
        "task": "left-tail loss",
        "confidence_levels": "one-in-a-hundred"
    }}
}}

Do not use your own explanation as evidence.
Evidence must come from the user's actual request.

INTERPRETATION RULES:

- Never invent assets.
- Assets are resolved deterministically elsewhere.
- Never overwrite deterministically resolved fields.
- Do not invent research parameters.
- If a parameter is unsupported, return null or [].
- Historical periods belong in lookback_days.
- Forward forecast/simulation periods belong in
  time_horizon_days.
- Monte Carlo language implies task "simulation".
- Explicit stress language implies task "stress_test".
- Downside, tail-risk, or left-tail language may imply
  task "risk_analysis".
- "one-in-a-hundred" loss implies approximately
  99% confidence.
- "one-in-twenty" loss implies approximately
  95% confidence.
- Confidence levels must be returned as decimals.
- Return JSON only.
"""


    def _build_request(
        self,
        data,
        baseline,
    ):
        """
        Merge grounded LLM interpretation with Athena's
        deterministic baseline.
        """

        # If Athena already knows the specialized task,
        # there is nothing for the LLM to override.

        if baseline.task != "general_analysis":
            return baseline

        resolved = set(
            baseline.resolved_fields
        )

        evidence = data.get(
            "evidence"
        )

        if not isinstance(
            evidence,
            dict,
        ):
            evidence = {}

        # -------------------------------------------------
        # Task
        # -------------------------------------------------

        task = self._resolve_task(
            data.get("task"),
            baseline.task,
        )

        # Task classification is allowed when the
        # deterministic parser could not classify the
        # request. Quantitative parameters below require
        # explicit evidence.

        # -------------------------------------------------
        # Assets
        # -------------------------------------------------

        # Asset identity is always deterministic.

        assets = list(
            baseline.assets
        )

        # -------------------------------------------------
        # Scenario
        # -------------------------------------------------

        scenario = baseline.scenario

        if (
            "scenario" not in resolved
            and self._evidence_supported(
                evidence.get("scenario")
            )
        ):
            candidate = (
                self._normalize_optional_string(
                    data.get("scenario")
                )
            )

            if candidate is not None:
                scenario = candidate

        # -------------------------------------------------
        # Lookback
        # -------------------------------------------------

        lookback_days = (
            baseline.lookback_days
        )

        if (
            "lookback_days" not in resolved
            and self._evidence_supported(
                evidence.get("lookback_days")
            )
        ):
            lookback_days = (
                self._positive_integer(
                    data.get("lookback_days"),
                    baseline.lookback_days,
                )
            )

        # -------------------------------------------------
        # Forward horizon
        # -------------------------------------------------

        time_horizon_days = (
            baseline.time_horizon_days
        )

        if (
            "time_horizon_days" not in resolved
            and self._evidence_supported(
                evidence.get(
                    "time_horizon_days"
                )
            )
        ):
            time_horizon_days = (
                self._positive_integer(
                    data.get(
                        "time_horizon_days"
                    ),
                    baseline.time_horizon_days,
                )
            )

        # -------------------------------------------------
        # Simulation count
        # -------------------------------------------------

        simulations = (
            baseline.simulations
        )

        if (
            "simulations" not in resolved
            and self._evidence_supported(
                evidence.get("simulations")
            )
        ):
            simulations = (
                self._positive_integer(
                    data.get("simulations"),
                    baseline.simulations,
                )
            )

        # -------------------------------------------------
        # Confidence
        # -------------------------------------------------

        confidence_levels = list(
            baseline.confidence_levels
        )

        if (
            "confidence_levels" not in resolved
            and self._evidence_supported(
                evidence.get(
                    "confidence_levels"
                )
            )
        ):
            candidate_confidence = (
                self._normalize_confidence_levels(
                    data.get(
                        "confidence_levels"
                    )
                )
            )

            if candidate_confidence:
                confidence_levels = (
                    candidate_confidence
                )

        # -------------------------------------------------
        # Models
        # -------------------------------------------------

        models = list(
            baseline.models
        )

        if (
            "models" not in resolved
            and self._evidence_supported(
                evidence.get("models")
            )
        ):
            candidate_models = (
                self._normalize_models(
                    data.get("models")
                )
            )

            if candidate_models:
                models = candidate_models

        # -------------------------------------------------
        # Metrics
        # -------------------------------------------------

        metrics = list(
            baseline.metrics
        )

        if (
            "metrics" not in resolved
            and self._evidence_supported(
                evidence.get("metrics")
            )
        ):
            candidate_metrics = (
                self._normalize_metrics(
                    data.get("metrics")
                )
            )

            if candidate_metrics:
                metrics = (
                    candidate_metrics
                )

        # Workflow defaults are deterministic behavior,
        # not invented user parameters.

        if not metrics:

            if task == "risk_analysis":
                metrics = [
                    "value_at_risk",
                    "expected_shortfall",
                ]

            elif task == "simulation":
                metrics = [
                    "returns",
                    "volatility",
                    "max_drawdown",
                ]

        # -------------------------------------------------
        # Comparison
        # -------------------------------------------------

        compare_assets = (
            baseline.compare_assets
        )

        if (
            "compare_assets" not in resolved
            and self._evidence_supported(
                evidence.get(
                    "compare_assets"
                )
            )
        ):
            candidate_compare = (
                self._normalize_boolean(
                    data.get(
                        "compare_assets"
                    )
                )
            )

            if candidate_compare is not None:

                compare_assets = (
                    candidate_compare
                    and len(assets) > 1
                )

        # -------------------------------------------------
        # Updated resolved fields
        # -------------------------------------------------

        enriched_fields = set(
            resolved
        )

        if task != "general_analysis":
            enriched_fields.add(
                "task"
            )

        # -------------------------------------------------
        # Final validated request
        # -------------------------------------------------

        return QuantRequest(
            task=task,
            assets=assets,
            scenario=scenario,
            lookback_days=lookback_days,
            time_horizon_days=time_horizon_days,
            simulations=simulations,
            confidence_levels=confidence_levels,
            models=models,
            metrics=metrics,
            compare_assets=compare_assets,
            resolved_fields=enriched_fields,
        )


    def _resolve_task(
        self,
        llm_task,
        baseline_task,
    ):
        """
        Validate an LLM task classification.
        """

        if not isinstance(
            llm_task,
            str,
        ):
            return baseline_task

        task = (
            llm_task
            .strip()
            .lower()
        )

        if task not in ALLOWED_TASKS:
            return baseline_task

        return task


    def _evidence_supported(
        self,
        evidence,
    ):
        """
        Verify that LLM evidence is literally grounded
        in the user's original request.
        """

        if evidence is None:
            return False

        if isinstance(
            evidence,
            list,
        ):
            evidence_values = evidence

        else:
            evidence_values = [
                evidence
            ]

        normalized_message = (
            self._normalize_evidence_text(
                self.current_message
            )
        )

        for value in evidence_values:

            if not isinstance(
                value,
                str,
            ):
                continue

            normalized_evidence = (
                self._normalize_evidence_text(
                    value
                )
            )

            if (
                normalized_evidence
                and normalized_evidence
                in normalized_message
            ):
                return True

        return False


    def _normalize_evidence_text(
        self,
        value,
    ):
        """
        Normalize user language and evidence so minor
        punctuation differences do not break matching.
        """

        if not isinstance(
            value,
            str,
        ):
            return ""

        value = value.lower()

        value = re.sub(
            r"[^a-z0-9]+",
            " ",
            value,
        )

        return " ".join(
            value.split()
        )


    def _positive_integer(
        self,
        value,
        default,
    ):
        """
        Validate positive integer parameters.
        """

        if value is None:
            return default

        try:
            value = int(
                value
            )

        except (
            TypeError,
            ValueError,
        ):
            return default

        if value <= 0:
            return default

        return value


    def _normalize_confidence_levels(
        self,
        values,
    ):
        """
        Normalize confidence values such as:

        0.95
        95
        [0.95, 0.99]
        [95, 99]
        """

        if values is None:
            return []

        if not isinstance(
            values,
            list,
        ):
            values = [
                values
            ]

        normalized = []

        for value in values:

            try:
                confidence = float(
                    value
                )

            except (
                TypeError,
                ValueError,
            ):
                continue

            if confidence > 1:
                confidence = (
                    confidence / 100
                )

            if not (
                0 < confidence < 1
            ):
                continue

            if confidence not in normalized:

                normalized.append(
                    confidence
                )

        return normalized


    def _normalize_models(
        self,
        models,
    ):
        """
        Normalize requested risk-model names.
        """

        if models is None:
            return []

        if not isinstance(
            models,
            list,
        ):
            models = [
                models
            ]

        normalized = []

        for model in models:

            if not isinstance(
                model,
                str,
            ):
                continue

            key = (
                model
                .strip()
                .lower()
            )

            model_name = (
                MODEL_ALIASES.get(
                    key
                )
            )

            if (
                model_name in ALLOWED_MODELS
                and model_name not in normalized
            ):
                normalized.append(
                    model_name
                )

        return normalized


    def _normalize_metrics(
        self,
        metrics,
    ):
        """
        Normalize requested metric names.
        """

        if metrics is None:
            return []

        if not isinstance(
            metrics,
            list,
        ):
            metrics = [
                metrics
            ]

        normalized = []

        for metric in metrics:

            if not isinstance(
                metric,
                str,
            ):
                continue

            key = (
                metric
                .strip()
                .lower()
                .replace(
                    "-",
                    " ",
                )
            )

            value = (
                METRIC_ALIASES.get(
                    key
                )
            )

            if (
                value
                and value not in normalized
            ):
                normalized.append(
                    value
                )

        return normalized


    def _normalize_boolean(
        self,
        value,
    ):
        """
        Normalize JSON-style booleans.
        """

        if isinstance(
            value,
            bool,
        ):
            return value

        if isinstance(
            value,
            str,
        ):

            lowered = (
                value
                .strip()
                .lower()
            )

            if lowered == "true":
                return True

            if lowered == "false":
                return False

        return None


    def _normalize_optional_string(
        self,
        value,
    ):
        """
        Normalize an optional string.
        """

        if not isinstance(
            value,
            str,
        ):
            return None

        value = value.strip()

        if not value:
            return None

        return value


    def _extract_json(
        self,
        response,
    ):
        """
        Extract a JSON object from model output.
        """

        if not isinstance(
            response,
            str,
        ):
            raise ValueError(
                "LLM response must be text."
            )

        cleaned = response.strip()

        cleaned = re.sub(
            r"<think>.*?</think>",
            "",
            cleaned,
            flags=re.DOTALL,
        )

        start = cleaned.find(
            "{"
        )

        end = cleaned.rfind(
            "}"
        )

        if (
            start == -1
            or end == -1
            or end < start
        ):
            raise ValueError(
                "No JSON found in LLM response."
            )

        data = json.loads(
            cleaned[
                start:end + 1
            ]
        )

        if not isinstance(
            data,
            dict,
        ):
            raise ValueError(
                "LLM response must contain a JSON object."
            )

        return data