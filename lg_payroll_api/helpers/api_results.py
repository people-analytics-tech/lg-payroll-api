from dataclasses import dataclass
from typing import List, Union, OrderedDict
from lg_payroll_api.utils.aux_types import EnumTipoDeRetorno, EnumOperacaoExecutada
from lg_payroll_api.utils.lg_exceptions import LgErrorException, LgInconsistencyException, LgNotProcessException


@dataclass(frozen=True)
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
        self.__raise_for_errors()
    
    @property
    def __unpacked_messages(self) -> str:
        return ' && '.join([" || ".join(value) for value in self.Mensagens.values()])

    def __raise_for_errors(self) -> None:
        if self.Tipo == EnumTipoDeRetorno.ERRO:
            raise LgErrorException(self.__unpacked_messages)
        
        elif self.Tipo == EnumTipoDeRetorno.INCONSISTENCIA:
            raise LgInconsistencyException(self.__unpacked_messages)
        
        elif self.Tipo == EnumTipoDeRetorno.NAO_PROCESSADO:
            raise LgNotProcessException(self.__unpacked_messages)


@dataclass(frozen=True)
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


@dataclass(frozen=True)
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
