from typing import Callable, Final, Optional

from inngest.helpers.strings import slugify
from inngest.types import FunctionConfig, FunctionConfigStep, FunctionConfigStepRuntime


class InngestFunction:
    step_id: Final = "step"

    def __init__(
        self,
        opts: dict,
        trigger: dict,
        fn: Callable,
    ) -> None:
        self._opts = opts
        self._trigger = trigger
        self._fn = fn

    def get_config(
        self,
        base_url: str,
        app_prefix: Optional[str],
    ) -> FunctionConfig:
        fn_id = self.id(app_prefix)
        step_url = base_url

        return FunctionConfig(
            id=fn_id,
            name=self.name,
            steps={
                self.step_id: FunctionConfigStep(
                    id=self.step_id,
                    name=self.step_id,
                    runtime=FunctionConfigStepRuntime(
                        type="http",
                        url=step_url,
                    ),
                )
            },
            triggers=[self._trigger],
        )

    def _generate_id(self, prefix: Optional[str]) -> str:
        return slugify("-".join([prefix or "", self._opts["name"]]))

    def id(self, prefix: Optional[str] = None) -> str:
        if not self._opts.get("id"):
            self._opts["id"] = self._generate_id(prefix)

        return self._opts["id"]

    @property
    def name(self) -> str:
        return self._opts["name"]

    def run_fn(self, data: object, op_stack: object) -> object:
        self._fn(data)


__all__ = ["InngestFunction"]
