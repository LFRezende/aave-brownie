from brownie import config, network, interface
from scripts.utils import getAccount, OTHER_CHAINS
from scripts.get_weth import get_weth
from web3 import Web3

AMOUNT = Web3.toWei(0.001, "ether")
riskFactor = "risky"


def main():
    account = getAccount()
    erc20_address = config["networks"][network.show_active()]["wethAddress"]
    print(f">>>>>> BALANCE OF ACCOUNT 1.1 : {account.balance()}")
    if network.show_active() in OTHER_CHAINS:
        get_weth()
    print(f">>>>>> BALANCE OF ACCOUNT 1.2: {account.balance()}")
    lending_pool = get_lending_pool()
    # ACCOUNT is approving AMOUNT of ERC 20 to be spent on the LENDING POOL.
    approve_erc20(AMOUNT, lending_pool.address, erc20_address, account)
    print(f">>>>>> BALANCE OF ACCOUNT 1.3: {account.balance()}")
    # Let's finally deposit some WETH.
    print(">>> Request for deposit")
    # Deposit AMOUNT of ERC20 into the contract, automatically minting aERC20
    # and depositing them on ACCOUNT.ADDRESS, signed from ACCOUNT. (0 is deprecated)
    tx = lending_pool.deposit(
        erc20_address, AMOUNT, account.address, 0, {"from": account}
    )
    tx.wait(1)
    print(">>> Deposit finalized!")
    # ^^ the deposit function
    borrow, debt = getAccountData(lending_pool, account)
    # We now wish to borrow some DAI
    # Always remember: config has no parenthesis!
    dai_eth_pricefeed_address = config["networks"][network.show_active()][
        "dai_eth_pricefeed_address"
    ]
    dai_eth_price = get_dai_eth_price(dai_eth_pricefeed_address)
    # Let's borrow some DAI
    amount_to_borrow = (1 / dai_eth_price) * borrow * safety(riskFactor)
    print(f"We're now going to borrow {amount_to_borrow:.5f} DAI!")
    # Borrow function requires the address of the token and the amount (IN WEI!!! of the TOKEN!!)
    dai_address = config["networks"][network.show_active()]["dai_token"]
    # borrow receives ADDRESS, AMOUNT IN WEI, INTEREST RATE (1 STABLE 2 VAR), REFCODE (DEP), ON BEHALF OF
    borrowTx = lending_pool.borrow(
        dai_address,
        Web3.toWei(amount_to_borrow, "ether"),
        1,
        0,
        account.address,
        {"from": account},
    )
    borrowTx.wait(1)
    getAccountData(lending_pool, account)
    repay_all(AMOUNT, lending_pool, account)
    print("All done, baby")


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
    print(erc20_address)
    erc20 = interface.IERC20(erc20_address)
    print(erc20)
    # approve spender to spend amount, I sign it - give its blessing.
    tx = erc20.approve(spender, amount, {"from": account})
    tx.wait(1)  # always wait a block after changing the blockchain
    print(tx)
    print(">>> Request Approved! <<<")
    return tx


# It is important to know certain data related to your assets.
# getUserAccountData returns a lot of stuff -> the collateral in eth,
# the debt in eth, how much you may still borrow, current liquidation threshold,
#
def getAccountData(lending_pool, account):
    """
    Return the data of the user while utilizing the Lending Pool
    """
    (
        collateral,
        debt,
        borrowable,
        threshold,
        ltv,
        health,
    ) = lending_pool.getUserAccountData(account.address)
    collateral = Web3.fromWei(collateral, "ether")
    debt = Web3.fromWei(debt, "ether")
    borrowable = Web3.fromWei(borrowable, "ether")
    print(f"Current amount deposited worth in ETH: {collateral}.")
    print(f"Current amount in debt worth in ETH: {debt}.")
    print(f"Current amount borrowable worth in ETH: {borrowable}.")
    return (float(borrowable), float(debt))


def get_dai_eth_price(dai_eth_pricefeed_address):
    """
    Interacts with the contract providing the DAI-ETH conversion rate.
    Since no imports are available due to the Lending Pool contract already being deployed, the function
    interacts with it via the AggregatorV3Interface in the interfaces library of Brownie.
    """
    dai_eth_pricefeed = interface.AggregatorV3Interface(dai_eth_pricefeed_address)
    dai_eth_price = Web3.fromWei(dai_eth_pricefeed.latestRoundData()[1], "ether")
    print(f"The current price of the asset is:  {dai_eth_price:.8f} ETH.")
    return float(dai_eth_price)


def safety(riskFactor):
    return config["riskFactor"][riskFactor]


def repay_all(amount, lending_pool, account):
    approve_erc20(
        Web3.toWei(amount, "ether"),
        lending_pool,
        config["networks"][network.show_active()]["dai_token"],
        account,
    )
    repayTx = lending_pool.repay(
        config["networks"][network.show_active()]["dai_token"],
        amount,
        1,
        account.address,
        {"from": account},
    )
    repayTx.wait(1)
