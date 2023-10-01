from dataclasses import dataclass


@dataclass
class ResultOfExchange:
    # TODO it must be replace with pydantic model and extend
    status_code: int
    result_message: str
