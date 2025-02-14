from typing import Literal

from zeep.helpers import serialize_object

from lg_payroll_api.helpers.api_results import (
    LgApiReturn,
    LgApiPaginationReturn,
    LgApiExecReturn
)
from lg_payroll_api.helpers.base_client import (
    BaseLgServiceClient,
    LgAuthentication
)
from lg_payroll_api.utils.enums import (
    get_enum_value,
    EnumTipoStatus,
    EnumTipoPonto,
    EnumGrauDeInstrucao,
    EnumMesesExperiencia,
    EnumModeloPosicao
)
from datetime import date


class LgApiPositionClient(BaseLgServiceClient):
    """LG API INFOS https://portalgentedesucesso.lg.com.br/api.aspx

    Default class to connect with the role endpoints, service "v1/ServicoDePosicao"
    """

    def __init__(self, lg_auth: LgAuthentication):
        super().__init__(lg_auth=lg_auth, wsdl_service="v1/ServicoDePosicao")
    
    @staticmethod
    def __bool_to_int(value: bool) -> int:
        if isinstance(value, bool):
            value = int(value)

        return value

    def consult_list(
        self,
        company_code: int,
        records_limit: int = 50,
        permission_to_recorded_employee: bool = None,
        only_actives: bool = None,
        consider_freeze: bool = None,
        only_officials: bool = None,
        not_temporaries: bool = None,
        search_term: str = None
    ) -> LgApiReturn:  
        permission_to_recorded_employee = self.__bool_to_int(permission_to_recorded_employee)
        only_actives = self.__bool_to_int(only_actives)
        consider_freeze = self.__bool_to_int(consider_freeze)
        only_officials = self.__bool_to_int(only_officials)
        not_temporaries = self.__bool_to_int(not_temporaries)

        params = {
            "QuantidadeDeItensRetornados": records_limit,
            "ComPermissaoParaCadastrarColaborador": permission_to_recorded_employee,
            "SomenteAtivos": only_actives,
            "ConsiderarPosicoesCongeladas": consider_freeze,
            "ConsiderarPosicoesApenasDoTipoOficial": only_officials,
            "ConsiderarPosicoesDiferentesDoTipoTemporaria": not_temporaries,
            "TermoDeBusca": search_term,
            "Empresa": {"Codigo": company_code}
        }

        return LgApiReturn(
            **serialize_object(
                self.send_request(
                    service_client=self.wsdl_client.service.ConsultarLista,
                    body=params,
                    parse_body_on_request=False
                )
            )
        )

    def consult_list_by_demand(
        self,
        company_code: int,
        search_term: str = None,
        permission_to_recorded_employee: bool = None,
        only_actives: bool = None,
        consider_freeze: bool = None,
        only_officials: bool = None,
        not_temporaries: bool = None,
    ) -> LgApiPaginationReturn:
        permission_to_recorded_employee = self.__bool_to_int(permission_to_recorded_employee)
        only_actives = self.__bool_to_int(only_actives)
        consider_freeze = self.__bool_to_int(consider_freeze)
        only_officials = self.__bool_to_int(only_officials)
        not_temporaries = self.__bool_to_int(not_temporaries)

        params = {
            "SomenteComPermissaoParaCadastrarColaborador": permission_to_recorded_employee,
            "SomenteAtivos": only_actives,
            "ConsiderarPosicoesCongeladas": consider_freeze,
            "ConsiderarPosicoesApenasDoTipoOficial": only_officials,
            "ConsiderarPosicoesDiferentesDoTipoTemporaria": not_temporaries,
            "TermoDaBusca": search_term,
            "Empresa": {"Codigo": company_code}
        }

        return LgApiPaginationReturn(
            auth=self.lg_client,
            wsdl_service=self.wsdl_client,
            service_client=self.wsdl_client.service.ConsultarListaPorDemanda,
            body=params,
            **serialize_object(
                self.send_request(
                    service_client=self.wsdl_client.service.ConsultarListaPorDemanda,
                    body=params,
                    parse_body_on_request=False
                )
            )
        )
    
    def consult(self, code: int) -> LgApiReturn:
        params = {"Codigo": code}
        return LgApiReturn(
            **serialize_object(
                self.send_request(
                    service_client=self.wsdl_client.service.Consultar,
                    body=params,
                    parse_body_on_request=False
                )
            )
        )
    
    def save(
        self,
        code: int,
        description: str,
        status: EnumTipoStatus,
        start_date: date,
        type: int,
        reason_code: int,
        end_date: date = None,
        jobs_quantity: int = None,
        enable_employee_enrollment: bool = None,
        is_key: bool = False,
        freeze: bool = False,
        freeze_end_date: date = None,
        company_code: int = None,
        office_code: int = None,
        work_local_code: str = None,
        tax_jurisdiction_code: int = None,
        cost_center_code: str = None,
        professional_nature_code: int = None,
        responsible_authority_code: int = None,
        permanent_role_code: int = None,
        commissioned_role_code: int = None,
        union_code: int = None,
        proffessional_liberal_union_code: int = None,
        organizational_unit_code: int = None,
        unique_combination: bool = False,
        timekeeping_required: bool = False,
        timekeeping_type: EnumTipoPonto = None,
        work_shift_code: str = None,
        function_code: int = None,
        commissioned_function_code: int = None,
        areas_of_expertise_list: list[int] = None,
        hierarchical_level_code: int = None,
        short_description: str = None,
        long_description: str = None,
        education_level: EnumGrauDeInstrucao = None,
        edication_notes: str = None,
        experience: EnumMesesExperiencia = None,
        experience_notes: str = None,
        competences_group_list: list[tuple[int, int]] = None,
        competences_profile_list: list[tuple[int, int, int]] = None,
        replicate_positions: bool = None,
        replication_context: EnumModeloPosicao = None,
        original_position_transfer_employees: bool = None,
        original_position_code: int = None,
        original_position_status: EnumTipoStatus = None,
        original_position_description: str = None,
    ) -> LgApiReturn:
        date_frmt = "%Y-%m-%d"
        if isinstance(start_date, date):
            start_date = start_date.strftime(date_frmt)

        if isinstance(end_date, date):
            end_date = end_date.strftime(date_frmt)

        if isinstance(freeze_end_date, date):
            freeze_end_date = freeze_end_date.strftime(date_frmt)

        enable_employee_enrollment = self.__bool_to_int(enable_employee_enrollment)
        is_key = self.__bool_to_int(is_key)
        freeze = self.__bool_to_int(freeze)
        unique_combination = self.__bool_to_int(unique_combination)
        timekeeping_required = self.__bool_to_int(timekeeping_required)
        original_position_transfer_employees = self.__bool_to_int(original_position_transfer_employees)

        status = get_enum_value(status)
        timekeeping_type = get_enum_value(timekeeping_type)
        education_level = get_enum_value(education_level)
        experience = get_enum_value(experience)
        replication_context = get_enum_value(replication_context)
        original_position_status = get_enum_value(original_position_status)

        params = {
            "DataInicial": start_date,
            "DataFinal": end_date,
            "TipoDaPosicao": {"Codigo": type},
            "MotivoDaPosicao": {"Codigo": reason_code},
            "ComposicaoDaPosicao": {
                "CodigoEmpresa": company_code,
                "CodigoEstabelecimento": office_code,
                "CodigoLocalDeTrabalho": work_local_code,
                "CodigoLotacaoTributaria": tax_jurisdiction_code,
                "CodigoCentroDeCusto": cost_center_code,
                "CodigoNaturezaProfissional": professional_nature_code,
                "CodigoOrgaoResponsavel": responsible_authority_code,
                "CodigoCargoEfetivo": permanent_role_code,
                "CodigoCargoComissionado": commissioned_role_code,
                "CodigoSindicato": union_code,
                "CodigoSindicatoProfissionalLiberal": proffessional_liberal_union_code,
                "CodigoUnidadeOrganizacional": organizational_unit_code,
                "CombinacaoUnica": unique_combination,
                "MarcaPonto": timekeeping_required,
                "TipoDePonto": timekeeping_type,
                "CodigoEscala": work_shift_code,
                "CodigoFuncao": function_code,
                "CodigoFuncaoComissionada": commissioned_function_code,
            },
            "PermiteCadastrarColaborador": enable_employee_enrollment,
            "EhChave": is_key,
            "CongelarPosicao": freeze,
            "DataFinalCongelamentoDaPosicao": freeze_end_date,
            "ListaDeAreaDeAtuacao": {
                "AreaAtuacaoPosicao": (
                    [{"Codigo": code} for code in areas_of_expertise_list]
                        if areas_of_expertise_list else None
                )
            },
            "NivelHierarquico": {"Codigo": hierarchical_level_code},
            "QuantidadeVagas": jobs_quantity,
            "Perfil": {
                "DadosGerais": {
                    "DescricaoResumida": short_description,
                    "DescricaoDetalhada": long_description,
                    "GrauDeInstrucao": education_level,
                    "ObservacaoEscolaridade": edication_notes,
                    "Experiencia": experience,
                    "ObservacaoExperiencia": experience_notes
                },
                "ListaPerfilGrupoDeCompetencias": {
                    "PerfilGrupoDeCompetenciasPosicao": (
                        [
                            {
                                "CodigoGrupoDeCompetencias": competence_group_code,
                                "Percentual": percent
                            } for competence_group_code, percent in competences_group_list
                        ] if competences_group_list else None
                    )
                },
                "ListaPerfilCompetencia": {
                    "PerfilCompetenciaPosicao": (
                        [
                            {
                                "Peso": weight,
                                "CodigoDaCompetencia": competence_code,
                                "CodigoDoGrupoDaCompetencia": competence_group_code
                            } for weight, competence_code, competence_group_code in competences_profile_list
                        ] if competences_profile_list else None
                    )
                }
            },
            "ReplicarPosicoes": {
                "PosicaoOriginal": {
                    "Descricao": original_position_description,
                    "Status": original_position_status,
                    "Codigo": original_position_code
                }
            } if replicate_positions else None,
            "Descricao": description,
            "Status": status,
            "Codigo": code
        }

        return LgApiExecReturn(
            **serialize_object(
                self.send_request(
                    service_client=self.wsdl_client.service.Salvar,
                    body=params,
                    parse_body_on_request=False
                )
            )
        )
    
    def delete(
        self,
        historical_start_date: date,
        code: int
    ) -> LgApiExecReturn:
        params = {
            "DataInicial": historical_start_date.strftime("%Y-%m-%d"),
            "Codigo": code
        }
        return LgApiExecReturn(
            **serialize_object(
                self.send_request(
                    service_client=self.wsdl_client.service.Excluir,
                    body=params,
                    parse_body_on_request=False
                )
            )
        )
