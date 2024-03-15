from typing import Union

from zeep import Client

from lg_payroll_api.helpers.authentication import LgAuthentication
from lg_payroll_api.utils.aux_functions import clean_none_values_dict


class BaseLgServiceClient:
    """LG API INFOS https://portalgentedesucesso.lg.com.br/api.aspx

    Default class to send requests to LG Soap API services
    """

    def __init__(self, lg_auth: LgAuthentication, wsdl_service: Union[str, Client]):
        super().__init__()
        self.lg_client = lg_auth
        if isinstance(wsdl_service, Client):
            self.wsdl_client: Client = wsdl_service

        elif isinstance(wsdl_service, str):
            self.wsdl_client: Client = Client(
                wsdl=f"{self.lg_client.base_url}/{wsdl_service}?wsdl"
            )

        else:
            raise ValueError("Wsdl must be zeep Client or String.")

    def send_request(
        self,
        service_client: Client,
        body: dict,
        parse_body_on_request: bool = False,
        send_none_values: bool = False,
    ):
        if not send_none_values:
            body = clean_none_values_dict(body)

        if parse_body_on_request:
            response = service_client(**body, _soapheaders=self.lg_client.auth_header)

        else:
            response = service_client(body, _soapheaders=self.lg_client.auth_header)

        return response
