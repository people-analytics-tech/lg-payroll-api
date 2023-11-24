from zeep.helpers import serialize_object

from lg_payroll_api.helpers.base_client import BaseLgServiceClient, LGAuthentication
from typing import Literal


class LgApiCostCenterClient(BaseLgServiceClient):
    """LG API INFOS https://portalgentedesucesso.lg.com.br/api.aspx

    Default class to connect with the center cost endpoints
    """

    def __init__(self, lg_auth: LGAuthentication):
        super().__init__(lg_auth=lg_auth, wsdl_service="v2/ServicoDeCentroDeCusto?wsdl")

    def find_cost_center(
        self,
        cc_code: str,
        permission_to_register: Literal[0, 1] = None,
        only_actives: Literal[0, 1] = None,
        company_code: int = None,
        page: int = None,
        get_all_pages: bool = False
    ) -> dict:
        """LG API INFOS https://portalgentedesucesso.lg.com.br/api.aspx

        Endpoint to get all center cost on LG System

        Return

        A List of OrderedDict that represents an Object(RetornoDeConsultaLista<CentroDeCusto>) API response
            [
                Tipo : int
                Mensagens : [string]
                CodigoDoErro : string
                CentroDeCusto : Object(CentroDeCusto)
            ]
        """
        params = {
            "TermoDaBusca": cc_code,
            "ComPermissaoParaCadastrarColaborador": permission_to_register,
            "SomenteAtivos": only_actives,
            "Empresa": company_code,
            "PaginaAtual": page
        }
        return serialize_object(
            self.send_request(
                service_client=self.wsdl_client.service.ConsultarListaPorDemanda,
                body=params,
            )
        )

    def cost_center_save(
        self,
        cost_center_inital_date: str,
        companies_code: list,
        cost_center_status: int,
        cost_center_description: str,
        cost_center_code: int,
        cost_center_allow_add_employee: int,
    ):
        """LG API INFOS https://portalgentedesucesso.lg.com.br/api.aspx

        Endpoint to create a center cost on LG System

        Returns:

        A OrderedDict that represents an Object(RetornoDeExecucao<CentroDeCustoV2>) API response
                {
                    OperacaoExecutada: : int
                    Codigo : string
                    CodigoDeIntegracao : string
                    Tipo : int
                    Mensagens : [string]
                    CodigoDoErro : string
                    CentroDeCustoV2 : Object(CentroDeCustoV2)
                }
        """
        return serialize_object(
            self.send_request(
                service_client=self.wsdl_client.service.Salvar,
                body={
                    "DataInicio": cost_center_inital_date,
                    "Empresas": companies_code,
                    "Status": cost_center_status,
                    "Descricao": cost_center_description,
                    "Codigo": cost_center_code,
                    "PermiteCadastrarColaborador": cost_center_allow_add_employee,
                },
            )
        )
