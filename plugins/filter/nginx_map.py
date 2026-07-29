from typing import Callable

from ansible.errors import AnsibleFilterError
from ansible.module_utils.common.text.converters import to_native
from pydantic import BaseModel, ConfigDict, ValidationError

# Link to official docs
# https://nginx.org/en/docs/stream/ngx_stream_map_module.html
# https://nginx.org/en/docs/http/ngx_http_map_module.html

class NginxMap(BaseModel):
    model_config = ConfigDict(extra='forbid')

    name: str
    source: str
    mappings: dict

    def get_align_mappings(self, indent: int) -> str:
        """Aligns the mappings with the longest hostname."""
        s = ""
        i = " " * indent
        max_length = max(len(hostname) for hostname in self.mappings)
        for hostname, value in self.mappings.items():
            s += i + f"{hostname:<{max_length}}{i}{value};\n"
        return s

    def render(self, indent: int) -> str:
        """Render the map block."""
        record = f"map {self.source} ${self.name}" + " {"
        record += "\n" + self.get_align_mappings(indent)
        record += "}"
        return record


class FilterModule(object):

    def filters(self) -> dict[str, Callable[..., str]]:
        return {'render_map_block': self.get_map_block}

    def get_ansible_error(self, e: ValidationError):
        for error in e.errors():
            return "Atribute '{0}' is not implemented to({1}): ".format(
                error['loc'][0], e.title) + error['msg']

    def get_map_block(
        self,
        nginx_map: dict,
        name: str,
        indent: int = 4,
    ) -> str:
        try:
            nginx_map['name'] = name
            ngx_map = NginxMap(**nginx_map)
            return ngx_map.render(indent=indent)
        except ValidationError as e:
            raise AnsibleFilterError("Filter failed: %s" %
                                     to_native(self.get_ansible_error(e)))
