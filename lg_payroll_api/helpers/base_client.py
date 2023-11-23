import time

from decouple import config
from zeep import Client

from lg_payroll_api.utils.lg_exceptions import (
    LgErrorException,
    LgInconsistencyException,
    LgNotProcessException,
    LGStatus,
)


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


class BaseLgServiceClient:
    """LG API INFOS https://portalgentedesucesso.lg.com.br/api.aspx

    Default class to connect with the companies endpoints
    """

    def __init__(self, lg_auth: LGAuthentication, wsdl_service: str):
        super().__init__()
        self.lg_client = lg_auth
        self.wsdl_client: Client = Client(wsdl=f"{self.lg_client.base_url}/{wsdl_service}")

    def send_request(self, service_client: Client, body: dict, parse_body_on_request: bool = False):
        #try:
        if parse_body_on_request:
            response = service_client(**body, _soapheaders=self.lg_client.auth_header)
        
        else:
            response = service_client(body, _soapheaders=self.lg_client.auth_header)

        #except Exception as e:
        #    print(
        #        f"Error in LG request: {e}. Wait {self.lg_client.retry_time_request} seconds for another try."
        #    )
        #    time.sleep(self.lg_client.retry_time_request)
        #    response = self.wsdl_client(**body, _soapheaders=self.lg_client.auth_header)

        return response


class Old(LGAuthentication):
    def __init__(self):
        super().__init__()
        self.environment_context = {"Ambiente": config("LG_API_AMBIENT_ID")}
        self.header_authentication = {
            "TokenUsuario": {
                "Senha": config("LG_API_PASSWORD"),
                "Usuario": config("LG_API_USER"),
                "GuidTenant": config("LG_API_GUID_TENANT"),
            }
        }
        self.headers = {
            "LGContextoAmbiente": self.environment_context,
            "LGAutenticacao": self.header_authentication,
        }
        self.base_url = config("LG_API_URL")
        self.retry_time_request = config("RETRY_TIME", default=60, cast=int)

    def check_movement_response(self, api_response):
        response_code = api_response.get("Tipo")
        if response_code != LGStatus.SUCCESS.value:
            if response_code == LGStatus.INCONSISTENCE.value:
                message = api_response.get("ListaDeRetorno")
                message = message.get("IdentificadorDeOcorrencias")[0]
                message = message.get("Mensagens")
                message = message.get("string")[0]
                raise LgInconsistencyException(message)
            elif response_code == LGStatus.ERROR.value:
                message = api_response.get("Mensagens")
                message = message.get("string")[0]
                raise LgErrorException(message)
            else:
                raise LgNotProcessException("Solicitação não processada")
