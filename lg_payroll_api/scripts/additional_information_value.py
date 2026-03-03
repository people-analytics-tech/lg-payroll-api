from zeep.helpers import serialize_object

from lg_payroll_api.helpers.api_results import LgApiReturn, LgApiSaveListReturn
from lg_payroll_api.helpers.base_client import BaseLgServiceClient, LgAuthentication
from lg_payroll_api.utils.enums import (
    EnumTipoEntidadeInformacaoAdicional, EnumIdentificadorInformacaoAdicional
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

    def consult_list_by_entity(
        self,
        entity_type: EnumIdentificadorInformacaoAdicional,
        company_code: int = None,
        entity_code: int = None
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
        if isinstance(entity_type, EnumIdentificadorInformacaoAdicional):
            entity_type = entity_type.value

        #Get the complex type for the entity
        InfoAdic = self.wsdl_client.get_type(f"{self.lg_dto}{entity_type}")
        #Contruct the type with info
        identificador = InfoAdic(
            Codigo=entity_code,
            CodigoEmpresa=company_code
        )
        # Create the payload with the complex type
        params = {
            "filtro": {
                "Identificador": identificador
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

    def save_additional_information_value(
        self,
        additional_info_code: int,
        additional_info_value: str,
        entity_code: int,
        entity_type: EnumIdentificadorInformacaoAdicional,
        company_code: int = None,
        selected_options: list[str] = None
    ) -> LgApiSaveListReturn:
        """Save additional information value in LG System

        Args:
            additional_info_code (int, mandatory): Additional information identifier;
            additional_info_value (str, mandatory): Value to be saved in the additional information;
            entity_code (int, mandatory): Identifier of the entity related to the additional information value;
            company_code (int, optional): Company code of the entity;
            entity_type (EnumIdentificadorInformacaoAdicional, mandatory): Type of the entity;
            selected_options (list[str], optional): List of selected options identifiers for the additional information value.

        Returns:
            LgApiSaveListReturn: An OrderedDict that represents an Object(RetornoDeExecucao) API response
                {
                    Tipo : int
                    Mensagens : [string]
                    CodigoDoErro : string
                }
        """
        if isinstance(entity_type, EnumIdentificadorInformacaoAdicional):
            entity_type = entity_type.value

        #Get the complex type for the entity
        InfoAdic = self.wsdl_client.get_type(f"{self.lg_dto}{entity_type}")
        #Contruct the type with info
        identificador = InfoAdic(
            Codigo=entity_code,
            CodigoEmpresa=company_code
        )
        # Create the payload with the complex type
        params = {
            "IdentificadorDaEntidade": identificador,
            "Codigo": additional_info_code,
            "Valor" : additional_info_value,
            "OpcoesSelecionadas": selected_options,
        }
        params = {
            "ValorDaInformacaoAdicional": [
                params
            ]
        }
        return LgApiSaveListReturn(
            **serialize_object(
                self.send_request(
                    service_client=self.wsdl_client.service.SalvarLista,
                    body=params,
                    parse_body_on_request=False,
                )
            )
        )

