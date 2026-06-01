from datetime import date

from zeep.helpers import serialize_object

from lg_payroll_api.helpers.api_results import (
    LgApiExecReturn,
    LgApiPaginationReturn,
    LgApiReturn,
)
from lg_payroll_api.helpers.base_client import BaseLgServiceClient, LgAuthentication
from lg_payroll_api.utils.aux_functions import bool_to_int
from lg_payroll_api.utils.enums import EnumTipoStatus, get_enum_value


class LgApiOfficeLocalClient(BaseLgServiceClient):
    """LG API INFOS https://portalgentedesucesso.lg.com.br/api.aspx

    Default class to connect with the office/establishment endpoints,
    service "v2/ServicoDeEstabelecimento"
    """

    def __init__(self, lg_auth: LgAuthentication):
        super().__init__(lg_auth=lg_auth, wsdl_service="v2/ServicoDeEstabelecimento")

    @staticmethod
    def __format_date(value) -> str:
        if isinstance(value, date):
            return value.strftime("%Y-%m-%d")

        return value

    def _build_establishment_body(
        self,
        status: EnumTipoStatus,
        start_date: date,
        type: int,
        company_code: int,
        permit_employee_registration: bool,
        use_default_additional_info: bool,
        code: int = None,
        integration_code: str = None,
        description: str = None,
        cnae_code: str = None,
        main_cnae_code: str = None,
        fap_suspension_code: str = None,
        rat_suspension_code: str = None,
        gps_code: str = None,
        fgts_account: dict = None,
        contact: dict = None,
        apprentice_via_educational_entity: bool = None,
        bank_data: dict = None,
        end_date: date = None,
        company_integration_code: str = None,
        address_neighborhood: str = None,
        address_post_office_box: str = None,
        address_cep: str = None,
        address_post_office_box_cep: str = None,
        address_complement: str = None,
        address_street: str = None,
        address_city_code: int = None,
        address_city_integration_code: str = None,
        address_country_code: int = None,
        address_country_integration_code: str = None,
        address_number: str = None,
        address_street_type: int = None,
        identification: str = None,
        cei_identification: str = None,
        apprentice_hiring_indicative: int = None,
        subscription: str = None,
        subscription_type: int = None,
        identification_type: int = None,
        apprentice_entities: list[dict] = None,
        collection_list: list[dict] = None,
        additional_info_values: list[dict] = None,
        legal_nature: str = None,
        apprentice_process_number: str = None,
        pcd_process_number: str = None,
        fap_process_number: str = None,
        rat_process_number: str = None,
        observation: str = None,
        philanthropy_exemption_percentage: float = None,
        timekeeping_register: int = None,
        caepf_type: int = None,
        pcd_hiring_type: int = None,
        fap_process_type: int = None,
        rat_process_type: int = None,
    ) -> dict:
        """Build the EstabelecimentoCompleto body shared by save and the
        registration/update validation endpoints."""
        address = {
            "Bairro": address_neighborhood,
            "CaixaPostal": address_post_office_box,
            "Cep": address_cep,
            "CepCaixaPostal": address_post_office_box_cep,
            "Complemento": address_complement,
            "Logradouro": address_street,
            "Municipio": {
                "Codigo": address_city_code,
                "CodigoDeIntegracao": address_city_integration_code,
                "Pais": {
                    "Codigo": address_country_code,
                    "CodigoDeIntegracao": address_country_integration_code,
                }
                if address_country_code or address_country_integration_code
                else None,
            }
            if address_city_code or address_city_integration_code
            else None,
            "Numero": address_number,
            "TipoDeLogradouro": address_street_type,
        }

        return {
            "estabelecimento": {
                "Codigo": code,
                "CodigoDeIntegracao": integration_code,
                "Status": get_enum_value(status),
                "Descricao": description,
                "CodigoCnae": cnae_code,
                "CodigoCnaePreponderante": main_cnae_code,
                "CodigoDeSuspensaoFap": fap_suspension_code,
                "CodigoDeSuspensaoRat": rat_suspension_code,
                "CodigoGPS": gps_code,
                "ContaFGTSEstabelecimento": fgts_account,
                "Contato": contact,
                "ContratacaoDeAprendizPorIntermedioEntidadeEducativa": bool_to_int(
                    apprentice_via_educational_entity
                ),
                "DadosBancarios": bank_data,
                "DataFinal": self.__format_date(end_date),
                "DataInicial": self.__format_date(start_date),
                "Empresa": {
                    "Codigo": company_code,
                    "CodigoDeIntegracao": company_integration_code,
                },
                "Endereco": address
                if address_street or address_cep or address_city_code
                else None,
                "Identificacao": identification,
                "IdentificacaoCEI": cei_identification,
                "IndicativoContratacaoAprendiz": apprentice_hiring_indicative,
                "Inscricao": subscription,
                "ListaDeEntidadeAprendizEstabelecimento": {
                    "EntidadeAprendizEstabelecimento": apprentice_entities
                }
                if apprentice_entities
                else None,
                "ListaRecolhimentoEstabelecimento": {
                    "RecolhimentoDoEstabelecimento": collection_list
                }
                if collection_list
                else None,
                "ListaValorDaInformacaoAdicional": {
                    "ValorDaInformacaoAdicional": additional_info_values
                }
                if additional_info_values
                else None,
                "NaturezaJuridica": legal_nature,
                "NumeroDoProcessoAprendiz": apprentice_process_number,
                "NumeroDoProcessoPcd": pcd_process_number,
                "NumeroProcessoFap": fap_process_number,
                "NumeroProcessoRat": rat_process_number,
                "Observacao": observation,
                "PercentualDeIsencaoFilantropia": philanthropy_exemption_percentage,
                "PermiteCadastrarColaborador": bool_to_int(
                    permit_employee_registration
                ),
                "RegistroDePonto": timekeeping_register,
                "Tipo": type,
                "TipoDeCAEPF": caepf_type,
                "TipoDeContratacaoPcd": pcd_hiring_type,
                "TipoDeIdentificacao": identification_type,
                "TipoDeInscricao": subscription_type,
                "TipoDeProcessoFap": fap_process_type,
                "TipoDeProcessoRat": rat_process_type,
                "UtilizarValorPadraoInformacaoAdicional": bool_to_int(
                    use_default_additional_info
                ),
            }
        }

    def _build_period_body(
        self,
        code: int,
        start_date: date,
        end_date: date = None,
        integration_code: str = None,
    ) -> dict:
        """Build the ObjetoComCodigoNumericoEPeriodoHistorico body shared by
        delete and the deletion validation endpoints."""
        return {
            "estabelecimento": {
                "Codigo": code,
                "CodigoDeIntegracao": integration_code,
                "DataInicio": self.__format_date(start_date),
                "DataFim": self.__format_date(end_date),
            }
        }

    def retrieve_office_local(self, company_code: int) -> LgApiReturn:
        """LG API INFOS https://portalgentedesucesso.lg.com.br/api.aspx

        Endpoint (ConsultarLista) to get the list of establishments of a company.

        Returns:

        A LgApiReturn that represents an OrderedDict of Object(Estabelecimento) API response
        """
        params = {
            "Empresa": {
                "Codigo": company_code,
            }
        }
        return LgApiReturn(
            **serialize_object(
                self.send_request(
                    service_client=self.wsdl_client.service.ConsultarLista,
                    body=params,
                )
            )
        )

    def consult(self, code: int, integration_code: str = None) -> LgApiReturn:
        """LG API INFOS https://portalgentedesucesso.lg.com.br/api.aspx

        Endpoint (Consultar) to retrieve a single establishment by code.

        Args:
            code (int, mandatory): The establishment code
            integration_code (str, optional): The establishment integration code

        Returns:
            LgApiReturn with a single Object(Estabelecimento) on Retorno
        """
        params = {"Codigo": code, "CodigoDeIntegracao": integration_code}
        return LgApiReturn(
            **serialize_object(
                self.send_request(
                    service_client=self.wsdl_client.service.Consultar,
                    body=params,
                )
            )
        )

    def consult_list_by_codes(self, codes: list[int]) -> LgApiReturn:
        """LG API INFOS https://portalgentedesucesso.lg.com.br/api.aspx

        Endpoint (ConsultarListaPorListaDeCodigo) to get a list of establishments
        from a list of codes.

        Args:
            codes (list[int], mandatory): The establishment codes to retrieve

        Returns:
            LgApiReturn with a list of Object(Estabelecimento) on Retorno
        """
        params = {"Codigos": {"int": codes}}
        return LgApiReturn(
            **serialize_object(
                self.send_request(
                    service_client=self.wsdl_client.service.ConsultarListaPorListaDeCodigo,
                    body=params,
                )
            )
        )

    def list_on_demand(
        self,
        company_code: int,
        only_actives: bool = None,
        only_with_employee_registration: bool = None,
        search_term: str = None,
        page: int = None,
    ) -> LgApiPaginationReturn:
        """LG API INFOS https://portalgentedesucesso.lg.com.br/api.aspx

        Endpoint (ConsulteListaPorDemanda) to get a paginated list of establishments.

        Args:
            company_code (int, mandatory): Filter by company code
            only_actives (bool, optional): Return only active establishments
            only_with_employee_registration (bool, optional): Return only establishments
                that allow employee registration
            search_term (str, optional): Search term
            page (int, optional): Page number to retrieve

        Returns:
            LgApiPaginationReturn with a list of Object(Estabelecimento) on Retorno
        """
        params = {
            "PaginaAtual": page,
            "Empresa": {"Codigo": company_code},
            "SomenteAtivos": bool_to_int(only_actives),
            "SomenteComPermissaoParaCadastrarColaborador": bool_to_int(
                only_with_employee_registration
            ),
            "TermoDaBusca": search_term,
        }
        return LgApiPaginationReturn(
            auth=self.lg_client,
            wsdl_service=self.wsdl_client,
            service_client=self.wsdl_client.service.ConsulteListaPorDemanda,
            body=params,
            **serialize_object(
                self.send_request(
                    service_client=self.wsdl_client.service.ConsulteListaPorDemanda,
                    body=params,
                )
            )
        )

    def list_complete_on_demand(
        self,
        company_code: int,
        only_actives: bool = None,
        only_with_employee_registration: bool = None,
        search_term: str = None,
        page: int = None,
        consult_additional_info: bool = False,
    ) -> LgApiPaginationReturn:
        """LG API INFOS https://portalgentedesucesso.lg.com.br/api.aspx

        Endpoint (ConsulteListaCompletoPorDemanda) to get a paginated list of
        complete establishments.

        Args:
            company_code (int, mandatory): Filter by company code
            only_actives (bool, optional): Return only active establishments
            only_with_employee_registration (bool, optional): Return only establishments
                that allow employee registration
            search_term (str, optional): Search term
            page (int, optional): Page number to retrieve
            consult_additional_info (bool, optional): Whether to consult additional information

        Returns:
            LgApiPaginationReturn with a list of Object(EstabelecimentoCompleto) on Retorno
        """
        params = {
            "PaginaAtual": page,
            "EhParaConsultarInformacaoAdicional": bool_to_int(consult_additional_info),
            "Empresa": {"Codigo": company_code},
            "SomenteAtivos": bool_to_int(only_actives),
            "SomenteComPermissaoParaCadastrarColaborador": bool_to_int(
                only_with_employee_registration
            ),
            "TermoDaBusca": search_term,
        }
        return LgApiPaginationReturn(
            auth=self.lg_client,
            wsdl_service=self.wsdl_client,
            service_client=self.wsdl_client.service.ConsulteListaCompletoPorDemanda,
            body=params,
            **serialize_object(
                self.send_request(
                    service_client=self.wsdl_client.service.ConsulteListaCompletoPorDemanda,
                    body=params,
                )
            )
        )

    def save(
        self,
        status: EnumTipoStatus,
        start_date: date,
        type: int,
        company_code: int,
        permit_employee_registration: bool,
        use_default_additional_info: bool,
        code: int = None,
        integration_code: str = None,
        description: str = None,
        cnae_code: str = None,
        main_cnae_code: str = None,
        fap_suspension_code: str = None,
        rat_suspension_code: str = None,
        gps_code: str = None,
        fgts_account: dict = None,
        contact: dict = None,
        apprentice_via_educational_entity: bool = None,
        bank_data: dict = None,
        end_date: date = None,
        company_integration_code: str = None,
        address_neighborhood: str = None,
        address_post_office_box: str = None,
        address_cep: str = None,
        address_post_office_box_cep: str = None,
        address_complement: str = None,
        address_street: str = None,
        address_city_code: int = None,
        address_city_integration_code: str = None,
        address_country_code: int = None,
        address_country_integration_code: str = None,
        address_number: str = None,
        address_street_type: int = None,
        identification: str = None,
        cei_identification: str = None,
        apprentice_hiring_indicative: int = None,
        subscription: str = None,
        subscription_type: int = None,
        identification_type: int = None,
        apprentice_entities: list[dict] = None,
        collection_list: list[dict] = None,
        additional_info_values: list[dict] = None,
        legal_nature: str = None,
        apprentice_process_number: str = None,
        pcd_process_number: str = None,
        fap_process_number: str = None,
        rat_process_number: str = None,
        observation: str = None,
        philanthropy_exemption_percentage: float = None,
        timekeeping_register: int = None,
        caepf_type: int = None,
        pcd_hiring_type: int = None,
        fap_process_type: int = None,
        rat_process_type: int = None,
    ) -> LgApiExecReturn:
        """LG API INFOS https://portalgentedesucesso.lg.com.br/api.aspx

        Endpoint (Salvar) to create or update an establishment on LG System.

        Args:
            status (EnumTipoStatus, mandatory): Establishment status
            start_date (date, mandatory): Start date of the establishment record
            type (int, mandatory): Establishment type code
            company_code (int, mandatory): Company code that owns the establishment
            permit_employee_registration (bool, mandatory): Allow employee registration
            use_default_additional_info (bool, mandatory): Use default additional information values
            code (int, optional): Establishment code (omit to create a new one)
            integration_code (str, optional): Establishment integration code
            description (str, optional): Establishment description
            fgts_account (dict, optional): FGTS account with keys
                {Codigo, DigitoVerificadorCodigo, DigitoVerificadorDoSequencial, Sequencial}
            contact (dict, optional): Contact with keys
                {Celular, DddCelular, DddTelefone, EmailCorporativo, Ramal, Telefone}
            bank_data (dict, optional): Bank data with keys
                {Agencia{Codigo, CodigoDeIntegracao}, Banco{Codigo, CodigoDeIntegracao, Pais},
                 Conta, Digito, FormaDePagamento, TipoDaConta, ChavePix, TipoChavePix}
            apprentice_entities (list[dict], optional): Each item {CNPJ, RazaoSocial}
            collection_list (list[dict], optional): Each item {Percentual, TipoDeRecolhimento}
            additional_info_values (list[dict], optional): Each item
                {Codigo, TipoDaEntidade, Valor, OpcoesSelecionadas{string: [...]}}
            (other optional fields map directly to the EstabelecimentoCompleto entity)

        Returns:
            LgApiExecReturn that represents an Object(RetornoDeExecucao) API response
        """
        params = self._build_establishment_body(
            status=status,
            start_date=start_date,
            type=type,
            company_code=company_code,
            permit_employee_registration=permit_employee_registration,
            use_default_additional_info=use_default_additional_info,
            code=code,
            integration_code=integration_code,
            description=description,
            cnae_code=cnae_code,
            main_cnae_code=main_cnae_code,
            fap_suspension_code=fap_suspension_code,
            rat_suspension_code=rat_suspension_code,
            gps_code=gps_code,
            fgts_account=fgts_account,
            contact=contact,
            apprentice_via_educational_entity=apprentice_via_educational_entity,
            bank_data=bank_data,
            end_date=end_date,
            company_integration_code=company_integration_code,
            address_neighborhood=address_neighborhood,
            address_post_office_box=address_post_office_box,
            address_cep=address_cep,
            address_post_office_box_cep=address_post_office_box_cep,
            address_complement=address_complement,
            address_street=address_street,
            address_city_code=address_city_code,
            address_city_integration_code=address_city_integration_code,
            address_country_code=address_country_code,
            address_country_integration_code=address_country_integration_code,
            address_number=address_number,
            address_street_type=address_street_type,
            identification=identification,
            cei_identification=cei_identification,
            apprentice_hiring_indicative=apprentice_hiring_indicative,
            subscription=subscription,
            subscription_type=subscription_type,
            identification_type=identification_type,
            apprentice_entities=apprentice_entities,
            collection_list=collection_list,
            additional_info_values=additional_info_values,
            legal_nature=legal_nature,
            apprentice_process_number=apprentice_process_number,
            pcd_process_number=pcd_process_number,
            fap_process_number=fap_process_number,
            rat_process_number=rat_process_number,
            observation=observation,
            philanthropy_exemption_percentage=philanthropy_exemption_percentage,
            timekeeping_register=timekeeping_register,
            caepf_type=caepf_type,
            pcd_hiring_type=pcd_hiring_type,
            fap_process_type=fap_process_type,
            rat_process_type=rat_process_type,
        )
        return LgApiExecReturn(
            **serialize_object(
                self.send_request(
                    service_client=self.wsdl_client.service.Salvar,
                    body=params,
                    parse_body_on_request=True,
                )
            )
        )

    def delete(
        self,
        code: int,
        start_date: date,
        end_date: date = None,
        integration_code: str = None,
    ) -> LgApiExecReturn:
        """LG API INFOS https://portalgentedesucesso.lg.com.br/api.aspx

        Endpoint (Excluir) to delete an establishment history period on LG System.

        Args:
            code (int, mandatory): Establishment code
            start_date (date, mandatory): Start date of the period to delete
            end_date (date, optional): End date of the period to delete
            integration_code (str, optional): Establishment integration code

        Returns:
            LgApiExecReturn that represents an Object(RetornoDeExecucao) API response
        """
        params = self._build_period_body(
            code=code,
            start_date=start_date,
            end_date=end_date,
            integration_code=integration_code,
        )
        return LgApiExecReturn(
            **serialize_object(
                self.send_request(
                    service_client=self.wsdl_client.service.Excluir,
                    body=params,
                    parse_body_on_request=True,
                )
            )
        )

    def validate_registration(
        self, impeditive: bool = True, **establishment_fields
    ) -> LgApiReturn:
        """LG API INFOS https://portalgentedesucesso.lg.com.br/api.aspx

        Endpoint (ValidarCadastroImpeditivo / ValidarCadastroNaoImpeditivo) to
        validate an establishment registration without persisting it.

        Args:
            impeditive (bool, optional): If True (default), uses the impeditive
                validation, otherwise the non-impeditive one
            **establishment_fields: Same fields accepted by `save`

        Returns:
            LgApiReturn with an Object(InconsistenciaAPI) on Retorno
        """
        params = self._build_establishment_body(**establishment_fields)
        service_client = (
            self.wsdl_client.service.ValidarCadastroImpeditivo
            if impeditive
            else self.wsdl_client.service.ValidarCadastroNaoImpeditivo
        )
        return LgApiReturn(
            **serialize_object(
                self.send_request(
                    service_client=service_client,
                    body=params,
                    parse_body_on_request=True,
                )
            )
        )

    def validate_update(
        self, impeditive: bool = True, **establishment_fields
    ) -> LgApiReturn:
        """LG API INFOS https://portalgentedesucesso.lg.com.br/api.aspx

        Endpoint (ValidarAtualizacaoImpeditivo / ValidarAtualizacaoNaoImpeditivo)
        to validate an establishment update without persisting it.

        Args:
            impeditive (bool, optional): If True (default), uses the impeditive
                validation, otherwise the non-impeditive one
            **establishment_fields: Same fields accepted by `save`

        Returns:
            LgApiReturn with an Object(InconsistenciaAPI) on Retorno
        """
        params = self._build_establishment_body(**establishment_fields)
        service_client = (
            self.wsdl_client.service.ValidarAtualizacaoImpeditivo
            if impeditive
            else self.wsdl_client.service.ValidarAtualizacaoNaoImpeditivo
        )
        return LgApiReturn(
            **serialize_object(
                self.send_request(
                    service_client=service_client,
                    body=params,
                    parse_body_on_request=True,
                )
            )
        )

    def validate_deletion(
        self,
        code: int,
        start_date: date,
        end_date: date = None,
        integration_code: str = None,
        impeditive: bool = True,
    ) -> LgApiReturn:
        """LG API INFOS https://portalgentedesucesso.lg.com.br/api.aspx

        Endpoint (ValidarExclusaoImpeditivo / ValidarExclusaoNaoImpeditivo) to
        validate an establishment deletion without persisting it.

        Args:
            code (int, mandatory): Establishment code
            start_date (date, mandatory): Start date of the period to delete
            end_date (date, optional): End date of the period to delete
            integration_code (str, optional): Establishment integration code
            impeditive (bool, optional): If True (default), uses the impeditive
                validation, otherwise the non-impeditive one

        Returns:
            LgApiReturn with an Object(InconsistenciaAPI) on Retorno
        """
        params = self._build_period_body(
            code=code,
            start_date=start_date,
            end_date=end_date,
            integration_code=integration_code,
        )
        service_client = (
            self.wsdl_client.service.ValidarExclusaoImpeditivo
            if impeditive
            else self.wsdl_client.service.ValidarExclusaoNaoImpeditivo
        )
        return LgApiReturn(
            **serialize_object(
                self.send_request(
                    service_client=service_client,
                    body=params,
                    parse_body_on_request=True,
                )
            )
        )
