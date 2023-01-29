# Borrowing-Lending Application
The focus and development of the project encompass the following:


1. Swaping ETH for WETH 
2. Depositing WETH into the contract of WETHGateway.
3. Purchase another token with our ETH collateral
4. Withdrawing the ETH deposited.

## Resources utilized

- For the application to work, we used the Weth Token address on the mainnet (for testing on the Mainnet-Fork) as well as on Goerli.


- The IWeth interface, from @PatrickAlphaC AAVE-BROWNIE repo, for accessing the functions of the token contract.

- The ILendingPool interface, to access the lending pool contract for AAVE.

- The Web3 Development Framework "Brownie" has been employed.



## Project

### 1. Swapping ETH for Wrapped ETH

At first, we need to swap ETH for WETH. We may do so via establishing connection between our contract and the WrappedETH smart contract - the ERC20 version of ETH, or WETH.

By utilizing the IWeth interface, provided by @Patrick_Alpha_C, we may import the contract address for WETH and use the interface function from brownie. The address is mapped by the brownie-config file, depending on the network (goerli or mainnet-fork).

We then deposit the desired amount into the contract. It will automatically make us withdraw the same amounth deposited, but in Wrapped Tokens.

### 2. Depositing WETH in the Lending Pool of AAVE

After swaping ETH for WETH via the get_weth function, we need to access the lending pool contract for AAVE for depositing WETH.

The Lending Pool Contract for AAVE allows us to make actions such as deposits, withdraws of tokens and so on.

Grabbing the address for the Lending Pool in the AAVE documentation, for mainnet and goerli, as well as the interface for 
this contract, we may proceed.





