from zeep.helpers import serialize_object

from lg_payroll_api.helpers.api_results import LgApiReturn, LgApiExecutionReturn
from lg_payroll_api.helpers.base_client import BaseLgServiceClient, LgAuthentication
from lg_payroll_api.utils.enums import (
    EnumTipoEntidadeInformacaoAdicional
)


class LgApiAdditionalInformationValueClient(BaseLgServiceClient):
    """LG API INFOS https://portalgentedesucesso.lg.com.br/api.aspx

    Default class to connect with the additional information value endpoints
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
        """Consult additional information values filtering by concept type,
        identifiers of concepts and identifiers of additional informations.

        Args:
            **concept_type _(EnumTipoEntidadeInformacaoAdicional, mandatory)_**: Additional
            information type;
            **concept_codes _(list[str], mandatory)_**: List of concept identifiers;
            **additional_informations_codes _(list[str], optional)_**: List of identifiers
            of additional informations.
        """
        if isinstance(concept_type, EnumTipoEntidadeInformacaoAdicional):
            concept_type = concept_type.value

        params = {"filtro": {
            "TipoConceito": concept_type,
            "IdentificadoresDoConceito": {"string": concept_codes},
            "IdentificadoresInformacoesAdicionais": {"string": additional_informations_codes}
        }}
        return LgApiReturn(
            **serialize_object(
                self.send_request(
                    service_client=self.wsdl_client.service.ConsulteListaPorConceitoEInformacao,
                    body=params,
                    parse_body_on_request=True,
                )
            )
        )

    # TODO fix the problem with payload sended
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
        """**WARNING**: This method is not working yet.

        LG API INFOS https://portalgentedesucesso.lg.com.br/api.aspx

        Endpoint to get list of additional informations values in LG System

        Returns:
            LgApiReturn: A List of OrderedDict that represents an Object(RetornoDeConsultaLista<ValorDaInformacaoAdicionalParcial>) API response
                [
                    Tipo : int
                    Mensagens : [string]
                    CodigoDoErro : string
                    Retorno : list[Object(ValorDaInformacaoAdicionalParcial)]
                ]
        """
        if isinstance(entity_type, EnumTipoEntidadeInformacaoAdicional):
            entity_type = entity_type.value

        params = {
            "filtro": {
                "Identificador": {
                    "TipoEntidade": entity_type,
                    "InfoAdicCentroDeCusto": {
                        "Codigo": cost_center_code,
                        "CodigoEmpresa": company_code,
                        "TipoEntidade": entity_type
                    } if cost_center_code else None,
                    "InfoAdicUnidadeOrganizacional": {
                        "Codigo": org_unit_code,
                        "CodigoEmpresa": company_code,
                        "TipoEntidade": entity_type
                    } if org_unit_code else None,
                    "InfoAdicEstabelecimento": {
                        "Codigo": office_code,
                        "CodigoEmpresa": company_code,
                        "TipoEntidade": entity_type
                    } if office_code else None,
                    "InfoAdicContratoDeTrabalho": {
                        "Matricula": contract_code,
                        "CodigoEmpresa": company_code if company_code else None,
                        "TipoEntidade": entity_type if contract_code else None
                    } if contract_code else None,
                    "InfoAdicPosicao": {
                        "Codigo": role_code,
                        "CodigoEmpresa": company_code if role_code else None,
                        "TipoEntidade": entity_type if role_code else None
                    } if role_code else None
                }
            }
        }

        return LgApiReturn(
            **serialize_object(
                self.send_request(
                    service_client=self.wsdl_client.service.ConsultarListaPorEntidade,
                    body=params,
                    parse_body_on_request=True,
                )
            )
        )

    # TODO fix the problem with payload sended
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
        """**WARNING**: This method is not working yet.
        """
        if isinstance(entity_type, EnumTipoEntidadeInformacaoAdicional):
            entity_type = entity_type.value

        params = {"valores": {"ValorDaInformacaoAdicional": [{
            "IdentificadorDaEntidade": {
                "Identificador": entity_type,
                "InfoAdicCentroDeCusto": {
                    "Codigo": cost_center_code,
                    "CodigoEmpresa": company_code,
                } if cost_center_code else None,
                "InfoAdicUnidadeOrganizacional": {
                    "Codigo": org_unit_code,
                    "CodigoEmpresa": company_code,
                } if org_unit_code else None,
                "InfoAdicEstabelecimento": {
                    "Codigo": office_code,
                    "CodigoEmpresa": company_code,
                } if office_code else None,
                "InfoAdicContratoDeTrabalho": {
                    "Matricula": contract_code,
                    "CodigoEmpresa": company_code,
                } if contract_code else None,
                "InfoAdicPosicao": {
                    "Codigo": role_code,
                    "CodigoEmpresa": company_code,
                } if role_code else None
            },
            "Codigo": code,
            "Valor": value
        }]}}

        return LgApiExecutionReturn(
            **serialize_object(
                self.send_request(
                    service_client=self.wsdl_client.service.SalvarLista,
                    body=params,
                    parse_body_on_request=True,
                )
            )
        )

