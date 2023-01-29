from brownie import config, network, interface
from scripts.utils import getAccount, OTHER_CHAINS
from scripts.get_weth import get_weth


def main():
    account = getAccount()
    erc20_address = config["networks"][network.show_active()]["wethAddress"]
    if network.show_active() in OTHER_CHAINS:
        get_weth()
    lending_pool = get_lending_pool()


def get_lending_pool():
    lending_pool_address_provider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_addresses_provider"]
    )
    lending_pool_address = lending_pool_address_provider.getLendingPool()
    # Grabbed the Address of the Lending Pool. Just need the ABI/Interface now so we can return the Lending Pool.
    # Remapped Interface and dependencies via - organization/repo@version and compiler/solc/remappings ..."@... = ..."
    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool


def approve_erc20():
    