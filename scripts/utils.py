from brownie import accounts, network, config

LOCAL_CHAINS = ["development"]
OTHER_CHAINS = ["mainnet-fork", "goerli"]


def getAccount(index=None, id=None):
    if index:
        return accounts[id]
    if id:
        account = accounts.load(id)
        return account
    if network.show_active() in LOCAL_CHAINS:
        return accounts[0]
    if network.show_active() in OTHER_CHAINS:
        account = accounts.add(config["wallets"]["from_key"])
        return account
