from zeep.helpers import serialize_object

from lg_payroll_api.helpers.api_results import LgApiReturn
from lg_payroll_api.helpers.base_client import BaseLgServiceClient, LgAuthentication

class LgApiRelativesClient(BaseLgServiceClient):
    def __init__(self, lg_auth: LgAuthentication):
        super().__init__(lg_auth=lg_auth, wsdl_service="v2/ServicoDeDependente")

    def list_dependents_by_cpf(
        self,
        cpf: str,
    ) -> LgApiReturn:
        """LG API INFOS https://portalgentedesucesso.lg.com.br/api.aspx

        Endpoint to get the list of dependents of an employee by CPF in LG System

        Args:
            cpf (str): CPF of the employee to query for dependents

        Returns:
            LgApiPaginationReturn: A List of OrderedDict that represents an Object(RetornoDeConsultaLista<DependenteV2>) API response
        """

        body = {
            "FiltroComCpf": {
                "Cpf": cpf
            }
        }

        return LgApiReturn(
            **serialize_object(
                self.send_request(
                    auth=self.lg_client,
                    wsdl_service=self.wsdl_client,
                    service_client=self.wsdl_client.service.ConsultarListaPeloCpfColaborador,
                    body=body
                )
            )
        )