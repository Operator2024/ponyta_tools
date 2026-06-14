from typing import Callable


class FilterModule(object):

    def filters(self) -> dict[str, Callable[..., str]]:
        return {'to_compose_vars': self.to_compose_vars}

    def to_compose_vars(self,
                        pipe: str,
                        suffix: str,
                        substitution: bool = True) -> str:
        """Return a string for docker-compose variables."""
        s = f"{pipe.upper()}_{suffix.upper()}"
        return f"${{{s}}}" if substitution else s
