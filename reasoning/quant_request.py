from dataclasses import dataclass, field


@dataclass
class QuantRequest:
    task: str

    assets: list[str] = field(
        default_factory=list
    )

    scenario: str | None = None

    lookback_days: int = 252

    time_horizon_days: int = 252

    simulations: int = 10000

    confidence_levels: list[float] = field(
        default_factory=lambda: [0.99]
    )

    models: list[str] = field(
        default_factory=list
    )

    metrics: list[str] = field(
        default_factory=list
    )

    compare_assets: bool = False

    # Fields that the deterministic parser
    # explicitly resolved from the user's words.
    #
    # This lets Athena distinguish:
    #
    # "default 365 days"
    #
    # from:
    #
    # "the user explicitly asked for 365 days"
    #
    # The LLM may fill unresolved fields, but it
    # may not overwrite resolved ones.

    resolved_fields: set[str] = field(
        default_factory=set,
        repr=False,
    )

    def summary(self):
        return {
            "task": self.task,
            "assets": self.assets,
            "scenario": self.scenario,
            "lookback_days": self.lookback_days,
            "time_horizon_days": self.time_horizon_days,
            "simulations": self.simulations,
            "confidence_levels": self.confidence_levels,
            "models": self.models,
            "metrics": self.metrics,
            "compare_assets": self.compare_assets,
        }