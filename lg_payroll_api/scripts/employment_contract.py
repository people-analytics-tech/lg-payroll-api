from zeep.helpers import serialize_object
from datetime import date

from lg_payroll_api.helpers.base_client import BaseLgServiceClient, LgAuthentication
from lg_payroll_api.helpers.api_results import LgApiReturn, LgApiPaginationReturn, LgApiExecutionReturn
from lg_payroll_api.utils.aux_types import SITUATIONS, EnumTipoDeDadosModificados, EnumTipoDeOperacaoContratoLog
from lg_payroll_api.utils.aux_functions import clean_none_values_dict

class LgApiEmploymentContract(BaseLgServiceClient):
    def __init__(self, lg_auth: LgAuthentication):
        super().__init__(lg_auth=lg_auth, wsdl_service="v2/ServicoDeContratoDeTrabalho")

    def get_employment_contract(self, contract_code: str, company_code: int) -> LgApiReturn:
        body = {
            "Colaborador": {
                "Matricula": contract_code,
                "Empresa": {
                    "Codigo": company_code
                }
            }
        }

        return LgApiReturn(**serialize_object(
            self.send_request(
                service_client=self.wsdl_client.service.Consultar,
                body=clean_none_values_dict(body),
            )
        ))

    def get_employment_contract_list_on_demand(self, employee_status: list[SITUATIONS] = None, current_page: int = None) -> LgApiPaginationReturn:
        body = {
            "TiposDeSituacoes": [{"int": situation} for situation in employee_status] if employee_status else None,
            "PaginaAtual": current_page,
        }
        return LgApiPaginationReturn(**serialize_object(
            self.send_request(
                service_client=self.wsdl_client.service.ConsultarListaPorDemanda,
                body=clean_none_values_dict(body),
            )
        ))

    def get_employee_manager(
        self,
        employee_code: str,
        employee_company_id: int,
        situations_types: list[SITUATIONS] = None
    ) -> LgApiReturn:
        body = {
            "TiposDeSituacoes": situations_types,
            "Colaborador": {
                "Matricula": employee_code,
                "Empresa": {"Codigo": employee_company_id},
            }
        }
        return LgApiReturn(**serialize_object(
            self.send_request(
                service_client=self.wsdl_client.service.ConsultarListaDeGestorImediato,
                body=clean_none_values_dict(body),
            )
        ))
    
    def get_updated_contracts(
        self,
        company_code: int,
        start_date: date,
        end_date: date,
        operations_types: list[EnumTipoDeOperacaoContratoLog] = [
            EnumTipoDeOperacaoContratoLog.INCLUSAO.value,
            EnumTipoDeOperacaoContratoLog.ALTERACAO.value,
            EnumTipoDeOperacaoContratoLog.EXCLUSAO.value,
        ],
        situation_type: list[SITUATIONS] = None,
        modified_data_type: EnumTipoDeDadosModificados = EnumTipoDeDadosModificados.CONTRATUAIS_E_PESSOAIS.value,
        enrollments: list[str] = None,
    ) -> LgApiReturn:
        body = {
            "filtro":{
                "TiposDeSituacao": situation_type,
                "TipoDeDadosModificados": modified_data_type,
                "TiposDeOperacoes": [{"TipoDeOperacao": {"Valor": operation}} for operation in operations_types],
                "CodigoDaEmpresa": company_code,
                "ListaDeMatriculas": enrollments,
                "PeriodoDeBusca": {
                    "DataInicio": start_date.strftime("%Y-%m-%d"),
                    "DataFim": end_date.strftime("%Y-%m-%d"),
                },
            }
        }
        return LgApiReturn(**serialize_object(
            self.send_request(
                service_client=self.wsdl_client.service.ConsultarListaDeModificados,
                body=clean_none_values_dict(body),
                parse_body_on_request=True
            )
        ))

    def post_employee_manager(
        self,
        employee_code: str,
        employee_company_id: int,
        manager_code: str,
        manager_company_id: int,
        start_date: date = None,
        end_date: date = None,
    ) -> LgApiExecutionReturn:
        body = {
            "ListaDeAssociacaoContratoGestor": {
                "FiltroDeAssociacaoContratoGestor": {
                    "Contrato": {
                        "Matricula": employee_code,
                        "Empresa": {
                            "Codigo": employee_company_id,
                        },
                    },
                    "Gestores": {
                        "FiltroComIdentificacaoDeContratoV2": {
                            "Matricula": manager_code,
                            "Empresa": {
                                "Codigo": manager_company_id
                            },
                        }
                    },
                }
            },
            "Periodo": {
                "DataInicio": start_date.strftime("%Y-%m-%d") if start_date else None,
                "DataFim": end_date.strftime("%Y-%m-%d") if end_date else None,
            },
        }
        return LgApiExecutionReturn(**serialize_object(
            self.send_request(
                service_client=self.wsdl_client.service.InserirGestoresNaFicha,
                body=clean_none_values_dict(body)
            )
        ))

    def delete_employee_manager(
        self,
        employee_code,
        employee_company_id,
        manager_code,
        manager_company_id,
        start_date=None,
        end_date=None,
    ) -> LgApiExecutionReturn:
        body = {
            "ListaDeAssociacaoContratoGestor": {
                "FiltroDeAssociacaoContratoGestor": {
                    "Contrato": {
                        "Matricula": employee_code,
                        "Empresa": {
                            "Codigo": employee_company_id
                        },
                    },
                    "Gestores": {
                        "FiltroComIdentificacaoDeContratoV2": {
                            "Matricula": manager_code,
                            "Empresa": {
                                "Codigo": manager_company_id
                            },
                        }
                    },
                }
            },
            "Periodo": {
                "DataInicio": start_date if start_date else None,
                "DataFim": end_date if end_date else None,
            },
        }
        return LgApiExecutionReturn(**serialize_object(
            self.send_request(
                service_client=self.wsdl_client.service.ExcluirGestoresNaFicha,
                body=clean_none_values_dict(body),
            )
        ))
