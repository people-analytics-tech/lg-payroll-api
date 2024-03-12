from lg_payroll_api.helpers import *
from lg_payroll_api.scripts import *


class LgApi:
    def __init__(self, auth: LgAuthentication) -> None:
        self.__auth: LgAuthentication = auth

    @property
    def cost_center_service(self) -> LgApiCostCenterClient:
        return LgApiCostCenterClient(self.__auth)

    @property
    def employment_contract_service(self) -> LgApiEmploymentContract:
        return LgApiEmploymentContract(self.__auth)

    @property
    def organizational_unit_service(self) -> LgApiOrganizationalUnitClient:
        return LgApiOrganizationalUnitClient(self.__auth)

    @property
    def company_service(self) -> LgApiCompanyClient:
        return LgApiCompanyClient(self.__auth)
