Feature: Application initialization

  @good_case
  Scenario: Connectivity to REST Api is established
    Given flask application tries to start on port "5000"
    When GET request is sent to "localhost:5000/swagger.json"
    Then status code is "200"

  @bad_case
  Scenario: Application fails to start due invalid port range
    Given flask application tries to start on port "100000"
    When flask application finishes with non-zero exit status
    Then "OverflowError: getsockaddrarg: port must be 0-65535" is logged in error message

  @bad_case
  Scenario: Application fails to start due invalid port type argument
    Given flask application tries to start on port "foo"
    When flask application finishes with non-zero exit status
    Then "Error: Invalid value for '--port'" is logged in error message


