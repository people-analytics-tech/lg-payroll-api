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
    LgTaskExecutionException,
    LgTaskCancelledException,
    LgTaskNotRespondingException,
    LgTaskCompletedWithInconsistenciesException,
    LgTaskNotCompletedYetException
)
from requests import get, Response
import re


@dataclass
class BaseLgApiReturn:
    """This dataclass represents a Lg Api Return object

    Attr:
        Tipo (EnumTipoDeRetorno): The returnal type code
        Mensagens (OrderedDict[str, List[str]]): Messages of requisition
        CodigoDoErro (str): Error code
    """

    Tipo: EnumTipoDeRetorno
    Mensagens: OrderedDict[str, List[str]]
    CodigoDoErro: str

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
class LgApiReturn(BaseLgApiReturn):
    """This dataclass represents a Lg Api Return object

    Attr:
        Tipo (EnumTipoDeRetorno): The returnal type code
        Mensagens (OrderedDict[str, List[str]]): Messages of requisition
        CodigoDoErro (str): Error code
        Retorno (Union[dict, OrderedDict, List[dict], List[OrderedDict], None]): Requisition result value
    """
    Retorno: Union[dict, OrderedDict, List[dict], List[OrderedDict], None]


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


@dataclass
class LgApiAsyncExecutionReturn(BaseLgApiReturn):
    IdTarefa: str


@dataclass
class LgApiAsyncConsultReturn(LgApiReturn):
    """This dataclass represents a Lg Api Async Consult Return Return object

    Attr:
        Tipo (EnumTipoDeRetorno): The returnal type code
        Mensagens (OrderedDict[str, List[str]]): Messages of requisition
        CodigoDoErro (str): Error code
        Retorno (Union[dict, OrderedDict, List[dict], List[OrderedDict], None]): Requisition result value
        StatusProcessamento(int): Processing status code.
    """
    StatusProcessamento: int

    def _raise_for_errors(self) -> None:
        super()._raise_for_errors()

        if self.StatusProcessamento == 3550: # Execution error
            raise LgTaskExecutionException(self.__unpacked_messages)

        elif self.StatusProcessamento == 3465: # Task cancelled
            raise LgTaskCancelledException(self.__unpacked_messages)

        elif self.StatusProcessamento == 14296: # Task not responding
            raise LgTaskNotRespondingException(self.__unpacked_messages)

        elif self.StatusProcessamento == 39470: # Task completed with errors
            raise LgTaskCompletedWithInconsistenciesException(self.__unpacked_messages)
    
    def check_processing_completed(self) -> bool:
        """Check if task process if completed."""
        return self.StatusProcessamento == 3551
    
    def request_file(self, encoding: str = "ISO-8859-1") -> Response:
        if not self.check_processing_completed():
            raise LgTaskNotCompletedYetException(f"Task is not completed yet. Please, wait a few seconds and try again.")

        response = get(self.Retorno["Url"], allow_redirects=True)
        response.raise_for_status()

        if encoding:
            response.encoding = encoding

        return response

    def download_bytes_content(self) -> bytes:
        return self.request_file().content

    def download_file(self, file_path: str = None) -> str:
        file_response = self.request_file()

        if not file_path:
            match = re.search(r"filename=(.+)$", file_response.headers.get("Content-Disposition"))

            if not match:
                raise ValueError("Error to define filename to this report.")

            file_path = match.group(1)

        with open(file_path, "wb") as f:
            f.write(file_response.content)

        return file_path
