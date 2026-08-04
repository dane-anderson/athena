from dataclasses import dataclass, field


@dataclass
class QuantRequest:

    task: str

    assets: list[str] = field(
        default_factory=list
    )

    scenario: str | None = None

    time_horizon_days: int = 252

    simulations: int = 10000

    metrics: list[str] = field(
        default_factory=list
    )


    def summary(self):

        return {
            "task": self.task,
            "assets": self.assets,
            "scenario": self.scenario,
            "time_horizon_days": self.time_horizon_days,
            "simulations": self.simulations,
            "metrics": self.metrics,
        }