from brownie import config, network, interface
from scripts.utils import getAccount, OTHER_CHAINS
from scripts.get_weth import get_weth
from web3 import Web3

AMOUNT = Web3.toWei(0.1, "ether")


def main():
    account = getAccount()
    erc20_address = config["networks"][network.show_active()]["wethAddress"]
    if network.show_active() in OTHER_CHAINS:
        get_weth()
    lending_pool = get_lending_pool()
    # ACCOUNT is approving AMOUNT of ERC 20 to be spent on the LENDING POOL.
    approve_erc20(AMOUNT, lending_pool.address, erc20_address, account)


def get_lending_pool():
    lending_pool_address_provider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_addresses_provider"]
    )
    lending_pool_address = lending_pool_address_provider.getLendingPool()
    # Grabbed the Address of the Lending Pool. Just need the ABI/Interface now so we can return the Lending Pool.
    # Remapped Interface and dependencies via - organization/repo@version and compiler/solc/remappings ..."@... = ..."
    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool


# Amount to be spent by spender; address of who we're allowing to spend our token;
# Address of the token erc20 we're allowing to be spent;
# Account for signing the transaction.


def approve_erc20(amount, spender, erc20_address, account):
    print(">>>  Request for Approval for Token Started   <<<")
    # ""Getting the ERC20 contract""
    erc20 = interface.IERC20(erc20_address)
    # approve spender to spent amount, I sign it - give its blessing.
    tx = erc20.approve(spender, amount, {"from": account})
    tx.wait(1)  # always wait a block after changing the blockchain
    print(">>> Request Approved! <<<")
    return tx
