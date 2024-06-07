from zeep.helpers import serialize_object

from lg_payroll_api.helpers.api_results import LgApiAsyncExecutionReturn, LgApiAsyncConsultReturn
from lg_payroll_api.helpers.base_client import BaseLgServiceClient, LgAuthentication


class LgReportServiceClient(BaseLgServiceClient):
    """Lg API report service client class to access report service endpoints.
    
    Reference: https://portalgentedesucesso.lg.com.br/api.aspx
    """

    def __init__(self, lg_auth: LgAuthentication):
        super().__init__(lg_auth=lg_auth, wsdl_service="v1/ServicoDeRelatorio")

    def consult_task(self, task_id: str) -> LgApiAsyncConsultReturn:
        params = {"IdTarefa": task_id}
        return LgApiAsyncConsultReturn(
            **serialize_object(
                self.send_request(
                    service_client=self.wsdl_client.service.ConsultarTarefa,
                    body=params,
                )
            )
        )

    def generate_report(self, company_code: int, report_parameters: list[dict]) -> LgApiAsyncExecutionReturn:
        params = {
            "Empresa": {"Codigo": company_code},
            "Relatorios": [{"Relatorio": rep_param} for rep_param in report_parameters]
        }
        return LgApiAsyncExecutionReturn(
            **serialize_object(
                self.send_request(
                    service_client=self.wsdl_client.service.GerarRelatorio,
                    body=params,
                )
            )
        )

    def generate_report_by_name(
        self, company_code: int, report_name: str, parameters: list[str] = None
    ) -> LgApiAsyncExecutionReturn:
        """LG API INFOS https://portalgentedesucesso.lg.com.br/api.aspx

        Args:
            company_id (int, mandatory): Id of company to generate report
            report_name (str, mandatory): Name of report

        Returns:

        A LgApiAsyncExecutionReturn that represents an Object(RetornoDeExecucaoAsync) API response
            [
                Tipo : int
                Mensagens : [string]
                CodigoDoErro : string
                Retorno : Object(Empresa)
            ]
        """
        params = {
            "Empresa": {"Codigo": company_code},
            "NomeDoRelatorio": report_name,
            "Parametros": parameters
        }

        return LgApiAsyncExecutionReturn(
            **serialize_object(
                self.send_request(
                    service_client=self.wsdl_client.service.GerarRelatorioPorNome,
                    body=params,
                )
            )
        )
