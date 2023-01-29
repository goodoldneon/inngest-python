import dataclasses
from typing import Optional



@dataclasses.dataclass
class FunctionConfigStepRuntime:
    type: str
    url: str


@dataclasses.dataclass
class FunctionConfigStep:
    id: str
    name: str
    runtime: FunctionConfigStepRuntime
    # retries


@dataclasses.dataclass
class FunctionConfig:
    id: str
    name: str
    steps: dict[str, FunctionConfigStep]
    triggers: list[dict]

#   triggers: FunctionTrigger[];
#   steps: Record<
#     string,
#     {
#       id: string;
#       name: string;
#       runtime: {
#         type: "http";
#         url: string;
#       };
#       retries?: {
#         attempts?: number;
#       };
#     }
#   >;
#   idempotency?: string;
#   throttle?: {
#     key?: string;
#     count: number;
#     period: TimeStr;
#   };


