from dataclasses import InitVar, dataclass
from typing import List, OrderedDict, Union

from zeep import Client
from zeep.helpers import serialize_object

from lg_payroll_api.helpers.base_client import BaseLgServiceClient, LgAuthentication
from lg_payroll_api.utils.aux_types import EnumOperacaoExecutada, EnumTipoDeRetorno
from lg_payroll_api.utils.lg_exceptions import (
    LgErrorException,
    LgInconsistencyException,
    LgNotProcessException,
)


@dataclass
class LgApiReturn:
    """This dataclass represents a Lg Api Return object

    Attr:
        Tipo (EnumTipoDeRetorno): The returnal type code
        Mensagens (OrderedDict[str, List[str]]): Messages of requisition
        CodigoDoErro (str): Error code
        Retorno (Union[dict, OrderedDict, List[dict], List[OrderedDict], None]): Requisition result value
    """

    Tipo: EnumTipoDeRetorno
    Mensagens: OrderedDict[str, List[str]]
    CodigoDoErro: str
    Retorno: Union[dict, OrderedDict, List[dict], List[OrderedDict], None]

    def __post_init__(self):
        self._raise_for_errors()

    @property
    def __unpacked_messages(self) -> str:
        return " && ".join([" || ".join(value) for value in self.Mensagens.values()])

    def _raise_for_errors(self) -> None:
        if self.Tipo == EnumTipoDeRetorno.ERRO:
            raise LgErrorException(self.__unpacked_messages)

        elif self.Tipo == EnumTipoDeRetorno.INCONSISTENCIA:
            raise LgInconsistencyException(self.__unpacked_messages)

        elif self.Tipo == EnumTipoDeRetorno.NAO_PROCESSADO:
            raise LgNotProcessException(self.__unpacked_messages)


@dataclass
class LgApiPaginationReturn(LgApiReturn):
    """This dataclass represents a Lg Api Pagination Return object

    Attr:
        Tipo (EnumTipoDeRetorno): The returnal type code
        Mensagens (OrderedDict[str, List[str]]): Messages of requisition
        CodigoDoErro (str): Error code
        Retorno (Union[dict, OrderedDict, List[dict], List[OrderedDict], None]): Requisition result value
        NumeroDaPagina (int): Number of page returned
        QuantidadePorPagina (int): Total number of pages
        TotalGeral (int): Total number of records
    """

    NumeroDaPagina: int
    QuantidadePorPagina: int
    TotalDePaginas: int = None
    TotalGeral: int = None
    auth: InitVar[LgAuthentication] = None
    wsdl_service: InitVar[Client] = None
    service_client: InitVar[Client] = None
    body: InitVar[dict] = None
    page_key: InitVar[str] = "PaginaAtual"

    def __post_init__(
        self,
        auth: LgAuthentication,
        wsdl_service: Client,
        service_client: Client,
        body: dict,
        page_key: str = "PaginaAtual",
    ):
        self.NumeroDaPagina += 1
        self.TotalDePaginas += 1
        self._base_lg_service = BaseLgServiceClient(
            lg_auth=auth, wsdl_service=wsdl_service
        )
        self._service_client: Client = service_client
        self._body = body
        self._page_key = page_key
        super().__post_init__()

    def __increment_result(self, result: OrderedDict):
        self.Tipo = result["Tipo"]
        self.Mensagens = result["Mensagens"]
        self._raise_for_errors()

        returnal = result["Retorno"]
        if isinstance(returnal, list):
            self.Retorno += returnal

        elif isinstance(returnal, dict) or isinstance(returnal, OrderedDict):
            for key, value in returnal.items():
                if isinstance(value, list):
                    self.Retorno[key] += value

                else:
                    raise ValueError(
                        """Is not possible to unpack "Retorno" to increment values."""
                    )

    def all(self) -> "LgApiPaginationReturn":
        while self.NumeroDaPagina <= (self.TotalDePaginas - 1):
            self.NumeroDaPagina += 1
            self._body[self._page_key] = self.NumeroDaPagina
            self.__increment_result(
                serialize_object(
                    self._base_lg_service.send_request(
                        service_client=self._service_client,
                        body=self._body,
                    )
                )
            )

        return self


@dataclass
class LgApiExecutionReturn(LgApiReturn):
    """This dataclass represents a Lg Api Executions Return object

    Attr:
        Tipo (EnumTipoDeRetorno): The returnal type code
        Mensagens (OrderedDict[str, List[str]]): Messages of requisition
        CodigoDoErro (str): Error code
        Retorno (Union[dict, OrderedDict, List[dict], List[OrderedDict], None]): Requisition result value
        OperacaoExecutada (EnumOperacaoExecutada): Code of execution type
        Codigo (str): Concept code
        CodigoDeIntegracao (str): Integration concept code
    """

    OperacaoExecutada: EnumOperacaoExecutada
    Codigo: str
    CodigoDeIntegracao: str
