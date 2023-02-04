// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

interface AggregatorV3Interface {

  function decimals()
    external
    view
    returns (
      uint8
    );

  function description()
    external
    view
    returns (
      string memory
    );

  function version()
    external
    view
    returns (
      uint256
    );

  function getRoundData(
    uint80 _roundId
  )
    external
    view
    returns (
      uint80 roundId,
      int256 answer,
      uint256 startedAt,
      uint256 updatedAt,
      uint80 answeredInRound
    );

  function latestRoundData()
    external
    view
    returns (
      uint80 roundId,
      int256 answer,
      uint256 startedAt,
      uint256 updatedAt,
      uint80 answeredInRound
    );

/* Text to self on why we're now using the interfaces, not directly importing from github

    Before, what we were doing was remapping the imports in the smart contract deployed, where we could
    say the location of the imported contract within the other contract.

    Here, we are not remapping it, since we cannot write it down on code on the original, already deployed 
    Lending Pool contract.

    We must access an already established contract in the chain.
    Therefore, either we use an interface or the ABI, as well as the address of the contract.
*/

}
