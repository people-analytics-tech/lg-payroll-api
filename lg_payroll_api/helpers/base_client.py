from zeep import Client
from lg_payroll_api.helpers.authentication import LGAuthentication


class BaseLgServiceClient:
    """LG API INFOS https://portalgentedesucesso.lg.com.br/api.aspx

    Default class to connect with the companies endpoints
    """

    def __init__(self, lg_auth: LGAuthentication, wsdl_service: str):
        super().__init__()
        self.lg_client = lg_auth
        self.wsdl_client: Client = Client(wsdl=f"{self.lg_client.base_url}/{wsdl_service}")

    def send_request(self, service_client: Client, body: dict, parse_body_on_request: bool = False):
        if parse_body_on_request:
            response = service_client(**body, _soapheaders=self.lg_client.auth_header)

        else:
            response = service_client(body, _soapheaders=self.lg_client.auth_header)

        return response
