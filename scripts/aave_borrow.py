from brownie import config, network, interface
from scripts.utils import getAccount, OTHER_CHAINS
from scripts.get_weth import get_weth


def main():
    account = getAccount()
    erc20 = config["networks"][network.show_active()]["wethAddress"]
    if network.show_active() in OTHER_CHAINS:
        get_weth()


def get_lending_pool():
    