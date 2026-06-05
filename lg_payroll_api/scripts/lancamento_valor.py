from typing import Union

from zeep.helpers import serialize_object

from lg_payroll_api.helpers.api_results import LgApiReturn
from lg_payroll_api.helpers.base_client import BaseLgServiceClient, LgAuthentication


class LgApiLancamentoValorClient(BaseLgServiceClient):
    """LG API INFOS https://portalgentedesucesso.lg.com.br/api.aspx

    Default class to connect with the value posting (Lançamento de Valor) endpoints
    """

    def __init__(self, lg_auth: LgAuthentication):
        super().__init__(lg_auth=lg_auth, wsdl_service="v2/ServicoDeLancamentoDeValor")

    def consult_list_by_concept(
        self,
        referencia: dict,
        codigo_folha: Union[int, None] = None,
        codigo_situacao: Union[int, None] = None,
        tipo_do_colaborador: Union[list[int], None] = None,
        tipo_do_conceito: Union[int, None] = None,
        lista_de_codigos_do_conceito: Union[list[str], None] = None,
    ) -> LgApiReturn:
        """Consult value posting list filtering by collective concept.

        Args:
            **referencia _(dict, mandatory)_**: Month/Year reference as {"Mes": int, "Ano": int};
            **codigo_folha _(int, optional)_**: Payroll code identifier;
            **codigo_situacao _(int, optional)_**: Situation code;
            **tipo_do_colaborador _(list[int], optional)_**: List of employee types
                (use EnumTipoColaboradorLancamento);
            **tipo_do_conceito _(int, optional)_**: Concept type
                (use EnumConceitosParaLancamentoDeValor);
            **lista_de_codigos_do_conceito _(list[str], optional)_**: List of concept codes.

        Returns:
            LgApiReturn: API response with value posting list
        """
        # Build body with filter structure
        body = {
            "filtro": {
                "Referencia": referencia,
                "CodigoFolha": codigo_folha,
                "CodigoSituacao": codigo_situacao,
                "TipoDoColaborador": (
                    [{"int": tipo} for tipo in tipo_do_colaborador]
                    if tipo_do_colaborador
                    else None
                ),
                "TipoDoConceito": tipo_do_conceito,
                "ListaDeCodigosDoConceito": (
                    [{"string": codigo} for codigo in lista_de_codigos_do_conceito]
                    if lista_de_codigos_do_conceito
                    else None
                ),
            }
        }

        return LgApiReturn(
            **serialize_object(
                self.send_request(
                    service_client=self.wsdl_client.service.ConsultarListaPorConceito,
                    body=body,
                    parse_body_on_request=True,
                )
            )
        )
