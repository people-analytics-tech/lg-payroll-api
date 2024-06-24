from typing import Union

from zeep.helpers import serialize_object

from lg_payroll_api.helpers.api_results import (
    LgApiAsyncConsultReturn,
    LgApiAsyncExecutionReturn,
)
from lg_payroll_api.helpers.base_client import BaseLgServiceClient, LgAuthentication
from lg_payroll_api.utils.aux_functions import read_json_file
from lg_payroll_api.utils.models import Relatorio


class ReportParameters:
    """Aux class to configure report parameters to generate reports in LG system."""

    reports: list[Relatorio] = []
    __from_to_keys = {
        "DtoRelatorio": "Relatorio",
        "EnumTipoArquivoGerado": "TipoArquivoGerado",
        "ListaDeTiposDeArquivosDisponiveisParaGeracao": "TiposDeArquivosDisponiveisParaGeracao",
        "ListaDeGruposDeParametros": "GruposDeParametros",
        "EnumTipoGrupoDeParametrosRelatorio": "TipoGrupoDeParametrosRelatorio",
        "ListaDeParametrosDeRelatorio": "ParametrosDeRelatorio",
        "ListaDeOpcoes": "Opcoes",
        "ListaDeValorePadroes": "ValoresPadroes",
        "ListaDeValoresSelecionados": "ValoresSelecionados",
        "ListaDeGrupoDeOrdenacao": "GruposDeOrdenacao",
    }
    __report_match_args: dict = Relatorio.match_args()

    def __init__(self, parameters: Union[list[Relatorio], list[dict]]) -> None:
        for arg in parameters:
            if isinstance(arg, dict):
                self.reports.append(Relatorio(**arg))

            elif isinstance(arg, Relatorio):
                self.reports.append(arg)

            else:
                raise ValueError(
                    "Arguments must be list of dicts or list of Relatorio."
                )

    @classmethod
    def __search_match_key(cls, search_key: str, match_args: dict = None) -> list:
        sub_match_args = (
            match_args.get(search_key, match_args)
            if match_args
            else cls.__report_match_args.get(search_key, cls.__report_match_args)
        )

        if isinstance(sub_match_args, dict):
            sub_match_args = sub_match_args[list(sub_match_args.keys())[0]]

        if search_key == "TiposDeArquivosDisponiveisParaGeracao":
            print("")
        for item in sub_match_args:
            found_key = False
            if isinstance(item, dict):
                if search_key in list(item.keys()):
                    found_key = True

                else:
                    sub_match_args = cls.__search_match_key(search_key, item)
                    if search_key in sub_match_args:
                        found_key = True

                if sub_match_args:
                    sub_match_args.append(search_key)
                break

            elif isinstance(item, str):
                found_key = item == search_key or search_key == Relatorio.__name__
                if found_key:
                    break

        if Relatorio.__name__ not in sub_match_args:
            sub_match_args.append(Relatorio.__name__)

        return sub_match_args if found_key else []

    @classmethod
    def __prepare_dict(cls, dictionary: dict, match_keys: list = None) -> dict:
        result = {}
        for key, value in dictionary.items():
            new_key = cls.__from_to_keys.get(key, key)
            new_match_keys = cls.__search_match_key(new_key)

            if new_match_keys:
                match_keys = new_match_keys
                sub_args = []

                match_keys += sub_args
                match_keys = match_keys if match_keys else []

            if new_key not in match_keys:
                continue

            if isinstance(value, dict):
                result[new_key] = cls.__prepare_dict(value, match_keys)

            elif isinstance(value, list) and value:
                if isinstance(value[0], dict):
                    result[new_key] = [
                        cls.__prepare_dict(item, match_keys) for item in value
                    ]

                else:
                    result[new_key] = value

            else:
                result[new_key] = value

        return result

    @classmethod
    def read_report_generator_json(
        cls, params: Union[list[dict], dict, str]
    ) -> "ReportParameters":
        """This method able you to use file "GereListaRelatorio.json", generated automatically into front of LG system
        when you generate a report into platform, as parameters to use in "LgReportServiceClient.generate_report"
        as the attribute report_parameters.

        Args:
            params (Union[list[dict], dict, str], mandatory): Parameters in the same format of "GereListaRelatorio.json". You
            can pass a file path if you prefer to store the json file locally to use as parameters.

        Return:
            ReportParameters
        """
        if isinstance(params, str):
            params = read_json_file(params)

        if isinstance(params, dict):
            formatted_dictionary = cls.__prepare_dict(params)

            formatted_dictionary = [formatted_dictionary]

        elif isinstance(params, list):
            formatted_dictionary = [
                cls.__prepare_dict(param)[Relatorio.__name__] for param in params
            ]

        return cls(formatted_dictionary)

    def get_formatted_parameters(self) -> list[dict]:
        """Return formatted parameters ready to be used in "LgReportServiceClient.generate_report" method."""
        return [report.as_dict() for report in self.reports]


class LgReportServiceClient(BaseLgServiceClient):
    """Lg API report service client class to access report service endpoints.

    This class able you to use report service to generate and consult reports in Lg system.

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

    def generate_report(
        self, company_code: int, report_parameters: Union[list[dict], ReportParameters]
    ) -> LgApiAsyncExecutionReturn:
        """Generate report with parameters configuration. You can create parameters configuration by
        following the oficial documentation, but we recommend to use the `ReportParameters` object to
        create your parameters configuration.

        Args:
            company_code (int, mandatory): Company code, this not affect filters in report.
            report_parameters (Union[list[dict], ReportParameters], mandatory): Parameters used to generate report.

        Return:
            LgApiAsyncExecutionReturn

        Usage Example:
            ```python
            # Example of parameters configuration using ReportParameters

            from lg_payroll_api import LgPayrollApi, LgAuthentication, ReportParameters

            # Set report parameters in variable
            # You can see that format in object lg_payroll_api.utils.models.Relatorio.
            # Alternatively, you can use the format automatically created when you generate a new report at front of system,
            # Getting the "GereListaRelatorio.json" file.
            parameters = [
                {
                    "Id": "123",
                    "Nome": "name.fpl",
                    "DescricaoRelatorio": "description",
                    "TipoArquivoGerado": 0,
                    "TiposDeArquivosDisponiveisParaGeracao": ["0"],
                    "GruposDeParametros": [
                        {
                            "TipoGrupoDeParametrosRelatorio": 0,
                            "Id": 0,
                            "Nome": "name",
                            "IndiceGrupo": 0,
                            "ParametrosDeRelatorio": [
                                {
                                    "IdRelatorio":"123",
                                    "Id":"id",
                                    "IndiceReal":0,
                                    "Nome":"name",
                                    "Descricao":"description",
                                    "Operacao":0,
                                    "TipoDeDado":0,
                                    "Tamanho":0,
                                    "MascaraFormatacao":"",
                                    "Opcional":True,
                                    "PodeConsultarValor":True,
                                    "PossuiDescricao":True,
                                    "CampoDefinidoPorFormula":False,
                                    "Opcoes": [],
                                    "RegrasDeAtivacao": [],
                                    "ValoresPadroes": [],
                                    "ValoresSelecionados": []
                                }
                            ]
                        }
                    ]
                }
            ]

            auth = LgAuthentication()
            lg_api = LgPayrollApi(auth)

            # Instantiate ReportParameters object passing parameters defined before
            report_params = ReportParameters(parameters)

            lg_api.report_service.generate_report(company_code=0, report_parameters=report_params)
            ```
        """
        if isinstance(report_parameters, ReportParameters):
            report_parameters = report_parameters.get_formatted_parameters()

        params = {
            "Empresa": {"Codigo": company_code},
            "Relatorios": {"Relatorio": report_parameters},
        }

        return LgApiAsyncExecutionReturn(
            report_service_class=self,
            **serialize_object(
                self.send_request(
                    service_client=self.wsdl_client.service.GerarRelatorio,
                    body=params,
                    send_none_values=True,
                )
            )
        )

    def generate_report_by_name(
        self, company_code: int, report_name: str, parameters: list[str] = None
    ) -> LgApiAsyncExecutionReturn:
        """LG API INFOS

        Args:
            company_id (int, mandatory): Id of company to generate report
            report_name (str, mandatory): Name of report
            parameters (list[str], optional): List of report parameters

        Returns:

        A LgApiAsyncExecutionReturn that represents an Object(RetornoDeExecucaoAsync) API response
            [
                Tipo : int
                Mensagens : [string]
                CodigoDoErro : string
                Retorno : Object(Empresa)
            ]

        Reference: https://portalgentedesucesso.lg.com.br/api.aspx
        """
        params = {
            "Empresa": {"Codigo": company_code},
            "NomeDoRelatorio": report_name,
            "Parametros": parameters,
        }

        return LgApiAsyncExecutionReturn(
            report_service_class=self,
            **serialize_object(
                self.send_request(
                    service_client=self.wsdl_client.service.GerarRelatorioPorNome,
                    body=params,
                )
            )
        )
