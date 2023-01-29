from scripts.utils import getAccount, config, network
from brownie import interface


def get_weth():
    """
    Swaps ETH for WETH by minting the last one.
    """
    account = getAccount()
    # Using the interface to establish contact with the WETHGateway 
    # desired_contract = interface.NamewithnodotSol(addressofdesiredcontract)
    weth = interface.IWeth(config["networks"][network.show_active()]["wethAddress"])
    tx = weth.deposit({"from": account, "value": 0.1* 10**18})
    tx.wait(1)
    print("\n>>>      Received 0.1 WETH       <<<\n")
    return tx


def main():
    get_weth()
