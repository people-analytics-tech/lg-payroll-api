from lg_payroll_api.helpers import LgAuthentication
from lg_payroll_api.scripts import (
    LgApiCostCenterClient,
    LgApiEmploymentContract,
    LgApiOrganizationalUnitClient,
    LgApiCompanyClient
)


class LgPayrollApi:
    """Interface to access endpoints."""
    def __init__(self, auth: LgAuthentication) -> None:
        self.__auth: LgAuthentication = auth

    @property
    def cost_center_service(self) -> LgApiCostCenterClient:
        """Access cost centers service methods."""
        return LgApiCostCenterClient(self.__auth)

    @property
    def employment_contract_service(self) -> LgApiEmploymentContract:
        """Access employment contracts service methods."""
        return LgApiEmploymentContract(self.__auth)

    @property
    def organizational_unit_service(self) -> LgApiOrganizationalUnitClient:
        """Access organizational units service methods."""
        return LgApiOrganizationalUnitClient(self.__auth)

    @property
    def company_service(self) -> LgApiCompanyClient:
        """Access companies service methods."""
        return LgApiCompanyClient(self.__auth)
