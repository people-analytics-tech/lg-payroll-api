from datetime import datetime

from zeep.helpers import serialize_object

from lg_payroll_api.helpers.api_results import LgApiPaginationReturn
from lg_payroll_api.helpers.base_client import BaseLgServiceClient, LgAuthentication

class LgApiVacationServiceClient(BaseLgServiceClient):
    """LG API INFOS https://portalgentedesucesso.lg.com.br/api.aspx

    Default class to connect with the organizational unit endpoints
    """

    def __init__(self, lg_auth: LgAuthentication):
        super().__init__(
            lg_auth=lg_auth, wsdl_service="v2/ServicoDeFerias"
        )

    def list_vacations(
        self,
        company_code: int,
        contract_list: list[str],
        start_date: datetime,
        end_date: datetime,
    ) -> LgApiPaginationReturn:
        """LG API INFOS https://portalgentedesucesso.lg.com.br/api.aspx

        Endpoint to get the list of vacations for multiple contracts in LG System

        Args:
            company_code (int): Company identifier
            contract_list (List[str]): List of employee contract numbers
            start_date (datetime): Start date of the period to query for vacations
            end_date (datetime): End date of the period to query for vacations

        Returns:
            LgApiPaginationReturn: A List of OrderedDict that represents an Object(RetornoDeConsultaLista<Ferias>) API response
        """

        params = {
            "FiltroComIdentificacaoDeContratoColetivoEPeriodo": {
                "CodigoDaEmpresa": company_code,
                "ListaDeMatriculas": contract_list,
                "Periodo": {
                    "StartDate": start_date.strftime('%Y-%m-%d'),
                    "EndDate": end_date.strftime('%Y-%m-%d')
                },
            }
        }

        return LgApiPaginationReturn(
            auth=self.lg_client,
            wsdl_service=self.wsdl_client,
            service_client=self.wsdl_client.service.ConsultarListaParaVariosContratos,
            body=params,
            **serialize_object(
                self.send_request(
                    service_client=self.wsdl_client.service.ConsultarListaParaVariosContratos,
                    body=params,
                )
            )
        )