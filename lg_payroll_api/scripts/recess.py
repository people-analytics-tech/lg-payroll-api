from datetime import datetime
from zeep.helpers import serialize_object

from lg_payroll_api.helpers.api_results import LgApiReturn
from lg_payroll_api.helpers.base_client import BaseLgServiceClient, LgAuthentication

class LgApiRecessClient(BaseLgServiceClient):
    def __init__(self, lg_auth: LgAuthentication):
        super().__init__(lg_auth=lg_auth, wsdl_service="v2/ServicoDeAfastamento")

    def list_recess(
        self,
        company_code: int,
        registration_list: list[str],
        start_date: datetime,
        end_date: datetime,
    ) -> LgApiReturn:
        """LG API INFOS https://portalgentedesucesso.lg.com.br/api.aspx

        Endpoint to get the list of recess occurrences for multiple contracts in LG System

        Args:
            company_code (int): Company identifier
            registration_list (list[str]): List of employee registration numbers
            start_date (datetime): Start date of the period to query for recesses
            end_date (datetime): End date of the period to query for recesses

        Returns:
            LgApiReturn: An OrderedDict that represents an Object(RetornoDeConsultaLista<Recesso>) API response
        """

        params = {
                "CodigoDaEmpresa": company_code,
                "ListaDeMatriculas": registration_list,
                "Periodo": {
                    "StartDate": start_date.strftime('%Y-%m-%d'),
                    "EndDate": end_date.strftime('%Y-%m-%d')
                },
            }

        return LgApiReturn(
            **serialize_object(
                self.send_request(
                    service_client=self.wsdl_client.service.ConsultarListaParaVariosContratos,
                    body=params,
                )
            )
        )