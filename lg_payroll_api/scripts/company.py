from zeep.helpers import serialize_object

from lg_payroll_api.helpers.base_client import BaseLgServiceClient, LGAuthentication


class LgApiCompanyClient(BaseLgServiceClient):
    """LG API INFOS https://portalgentedesucesso.lg.com.br/api.aspx

    Default class to connect with the companies endpoints
    """

    def __init__(self, lg_auth: LGAuthentication):
        super().__init__(lg_auth=lg_auth, wsdl_service="v1/ServicoDeEmpresa?wsdl")

    def company_list(self, companies_code: list[int] = None, subscriptions_code: list[str] = None) -> dict:
        """LG API INFOS https://portalgentedesucesso.lg.com.br/api.aspx

        Endpoint to get list of companies on LG System

        Returns:

        A List of OrderedDict that represents an Object(RetornoDeConsultaLista<Empresa>) API response
            [
                Tipo : int
                Mensagens : [string]
                CodigoDoErro : string
                Empresa : Object(Empresa)
            ]
        """
        #if companies_code is None and subscriptions_code is None:
        #    companies_code = []

        params = {
            "FiltroDeEmpresaPorListaDeCodigoOuInscricao": {
                "ListaDeCodigos": companies_code,
                "ListaDeInscricoes": subscriptions_code
            }
        }

        return serialize_object(
            self.send_request(
                service_client=self.wsdl_client.service.ConsultarLista,
                body=params,
            )
        )
    
    def retrieve_company(self, company_code: int, integration_code: str = None) -> dict:
        params = {
            "Codigo": company_code,
            "CodigoDeIntegracao": integration_code
        }
        return self.send_request(
            service_client=self.wsdl_client.service.Consultar,
            body=params,
        )
