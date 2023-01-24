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

After swaping ETH for WETH via the get_weth function, we need to access the lending pool contract for AAVE for depositing WETH.

The Lending Pool Contract for AAVE allows us to make actions such as deposits, withdraws of tokens and so on.

Grabbing the address for the Lending Pool in the AAVE documentation, for mainnet and goerli, as well as the interface for 
this contract, we may proceed.





