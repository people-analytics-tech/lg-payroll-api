from zeep.helpers import serialize_object

from lg_payroll_api.helpers.api_results import LgApiReturn, LgApiExecutionReturn
from lg_payroll_api.helpers.base_client import BaseLgServiceClient, LgAuthentication
from lg_payroll_api.utils.enums import (
    EnumTipoEntidadeInformacaoAdicional
)


class LgApiAdditionalInformationValueClient(BaseLgServiceClient):
    """LG API INFOS https://portalgentedesucesso.lg.com.br/api.aspx

    Default class to connect with the organizational unit endpoints
    """
    def __init__(self, lg_auth: LgAuthentication):
        super().__init__(
            lg_auth=lg_auth, wsdl_service="v1/ServicoDeValorDaInformacaoAdicional"
        )

    def consult_list_concept_and_info(
        self,
        concept_type: EnumTipoEntidadeInformacaoAdicional,
        concept_codes: list[str],
        additional_informations_codes: list[str] = None
    ) -> LgApiReturn:
        params = {
            "TipoConceito": concept_type,
            "IdentificadoresDoConceito": concept_codes,
            "IdentificadoresInformacoesAdicionais": additional_informations_codes
        }
        return LgApiReturn(
            **serialize_object(
                self.send_request(
                    service_client=self.wsdl_client.service.ConsulteListaPorConceitoEInformacao,
                    body=params,
                    parse_body_on_request=False,
                )
            )
        )

    def consult_list_by_entity(
        self,
        entity_type: EnumTipoEntidadeInformacaoAdicional = None,
        company_code: int = None,
        org_unit_code: int = None,
        role_code: int = None,
        office_code: int = None,
        cost_center_code: str = None,
        contract_code: str = None,
    ) -> LgApiReturn:
        """LG API INFOS https://portalgentedesucesso.lg.com.br/api.aspx

        Endpoint to get list of organizational units in LG System

        Returns:
            LgApiReturn: A List of OrderedDict that represents an Object(RetornoDeConsultaLista<UnidadeOrganizacionalParcial>) API response
                [
                    Tipo : int
                    Mensagens : [string]
                    CodigoDoErro : string
                    Retorno : list[Object(UnidadeOrganizacionalParcial)]
                ]
        """
        params = {
            "Identificador": {
                "TipoEntidade": int(entity_type),
                "InfoAdicCentroDeCusto": {
                    "Codigo": cost_center_code,
                    "CodigoEmpresa": company_code,
                    "TipoEntidade": entity_type
                },
                "InfoAdicUnidadeOrganizacional": {
                    "Codigo": org_unit_code,
                    "CodigoEmpresa": company_code,
                    "TipoEntidade": entity_type
                },
                "InfoAdicEstabelecimento": {
                    "Codigo": office_code,
                    "CodigoEmpresa": company_code,
                    "TipoEntidade": entity_type
                },
                "InfoAdicContratoDeTrabalho": {
                    "Matricula": contract_code,
                    "CodigoEmpresa": company_code,
                    "TipoEntidade": entity_type
                },
                "InfoAdicPosicao": {
                    "Codigo": role_code,
                    "CodigoEmpresa": company_code,
                    "TipoEntidade": entity_type
                }
            }
        }

        return LgApiReturn(
            **serialize_object(
                self.send_request(
                    service_client=self.wsdl_client.service.ConsultarListaPorEntidade,
                    body=params,
                    parse_body_on_request=False,
                )
            )
        )

    def save_additional_information_value(
        self,
        code: int,
        value: str,
        entity_type: EnumTipoEntidadeInformacaoAdicional = None,
        company_code: int = None,
        org_unit_code: int = None,
        role_code: int = None,
        office_code: int = None,
        cost_center_code: str = None,
        contract_code: str = None,
    ) -> LgApiExecutionReturn:
        params = {
            "ValorDaInformacaoAdicionalV2": {
                "IdentificadorDaEntidade": {
                    "TipoEntidade": int(entity_type),
                    "InfoAdicCentroDeCusto": {
                        "Codigo": cost_center_code,
                        "CodigoEmpresa": company_code,
                        "TipoEntidade": entity_type
                    },
                    "InfoAdicUnidadeOrganizacional": {
                        "Codigo": org_unit_code,
                        "CodigoEmpresa": company_code,
                        "TipoEntidade": entity_type
                    },
                    "InfoAdicEstabelecimento": {
                        "Codigo": office_code,
                        "CodigoEmpresa": company_code,
                        "TipoEntidade": entity_type
                    },
                    "InfoAdicContratoDeTrabalho": {
                        "Matricula": contract_code,
                        "CodigoEmpresa": company_code,
                        "TipoEntidade": entity_type
                    },
                    "InfoAdicPosicao": {
                        "Codigo": role_code,
                        "CodigoEmpresa": company_code,
                        "TipoEntidade": entity_type
                    }
                },
                "Codigo": code,
                "Valor": value
            }
        }

        return LgApiExecutionReturn(
            **serialize_object(
                self.send_request(
                    service_client=self.wsdl_client.service.SalvarLista,
                    body=params,
                    parse_body_on_request=False,
                )
            )
        )

