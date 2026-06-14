from typing import Callable, Optional

from ansible.errors import AnsibleFilterError
from ansible.module_utils.common.text.converters import to_native
from pydantic import BaseModel, ConfigDict, Field, ValidationError

# Link to official docs
# https://nginx.org/en/docs/http/ngx_http_upstream_module.html


class HTTPServerUpstream(BaseModel):
    model_config = ConfigDict(extra='forbid')

    max_fails: Optional[int] = Field(default=1, ge=0)
    max_conns: Optional[int] = Field(None, ge=0)
    fail_timeout: Optional[str] = Field(None)
    weight: Optional[int] = Field(default=1, ge=1)
    server: str
    backup: bool = Field(default=False)

    def get_server_block(self) -> str:
        record = f"server {self.server}"
        if self.backup:
            record += " backup"
        if self.max_fails is not None:
            record += f" max_fails={self.max_fails}"
        if self.fail_timeout is not None:
            record += f" fail_timeout={self.fail_timeout}"
        if self.max_conns is not None:
            record += f" max_conns={self.max_conns}"
        if self.weight is not None:
            record += f" weight={self.weight}"
        return record


class Upstream(BaseModel):
    model_config = ConfigDict(extra='forbid')

    resolver: Optional[str] = Field(None)
    resolver_timeout: Optional[str] = Field(None)
    servers: list[HTTPServerUpstream]

    def render(self) -> str:
        record = ""
        for attr_name, attr_value in self.__dict__.items():
            if not isinstance(attr_value, list) and attr_value is not None:
                record += f"{attr_name} {attr_value};\n"
        if record:
            record += "\n"
        for server in self.servers:
            record += f"{server.get_server_block()};\n"
        return record


class FilterModule(object):

    def filters(self) -> dict[str, Callable[..., str]]:
        return {'render_upstream_block': self.get_upstream_block}

    def get_ansible_error(self, e: ValidationError):
        for error in e.errors():
            loc_msg = error['loc'][0] if 0 > len(
                error['loc']) < 3 else error['loc'][2]
            return "Atribute '{0}' is not implemented to({1}): ".format(
                loc_msg, e.title) + error['msg']

    def get_upstream_block(self, upstream: dict) -> str:
        try:
            u = Upstream(**upstream)
            return u.render()
        except ValidationError as e:
            raise AnsibleFilterError("Filter failed: %s" %
                                     to_native(self.get_ansible_error(e)))
