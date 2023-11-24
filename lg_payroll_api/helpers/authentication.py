class LGAuthentication:
    base_url: str = None
    retry_time_request: int = None

    def __init__(
        self,
        base_url: str,
        user: str,
        password: str,
        guild_tenant: str,
        environment_context: int,
        retry_time_request: int = 60
    ) -> None:
        self.base_url = base_url
        self.user = user
        self.password = password
        self.guild_tenant = guild_tenant
        self.environment_context = environment_context
    

    @property
    def auth_header(self) -> dict:
        """Return a auth header to xml body in json format."""

        environment: dict = {"Ambiente": self.environment_context}

        header_authentication = {
            "TokenUsuario": {
                "Senha": self.password,
                "Usuario": self.user,
                "GuidTenant": self.guild_tenant,
            }
        }

        return {
            "LGContextoAmbiente": environment,
            "LGAutenticacao": header_authentication,
        }
