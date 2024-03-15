from enum import Enum
from typing import Literal

SITUATIONS = Literal["Afastamento", "Atividade normal", "Férias", "Recesso", "Rescisão"]


class EnumTipoDeDadosModificados(int, Enum):
    CONTRATUAIS = 1
    PESSOAIS = 2
    CONTRATUAIS_E_PESSOAIS = 3


class EnumTipoDeOperacao(int, Enum):
    INCLUSAO = 1
    ALTERACAO = 2
    EXCLUSAO = 3


class EnumTipoDeOperacaoContratoLog(int, Enum):
    INCLUSAO = 1
    ALTERACAO = 2
    EXCLUSAO = 3


class EnumTipoDeDadosModificadosDaUnidadeOrganizacional(int, Enum):
    DADOS_QUE_ALTERAM_HIERARQUIA = 1


class EnumTipoDeRetorno(int, Enum):
    SUCESSO = 0
    INCONSISTENCIA = 1
    ERRO = 2
    NAO_PROCESSADO = 3


class EnumOperacaoExecutada(int, Enum):
    NENHUM = 0
    OBJETO_SEM_ALTERACAO = 1
    CADASTRO = 2
    ATUALIZACAO = 3
    EXCLUSAO = 4
    CADASTRO_EM_LOTE = 5
    VALIDACAO = 6
