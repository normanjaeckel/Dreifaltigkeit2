module MainTest exposing (suite)

import Expect
import Main exposing (stringJoinIfNotEmpty)
import Test exposing (Test, describe, test)


suite : Test
suite =
    describe "stringJoinIfNotEmpty"
        [ test "does join two elements" <|
            \_ ->
                stringJoinIfNotEmpty " · " [ "one", "two" ]
                    |> Expect.equal "one · two"
        , test "does not join first empty element" <|
            \_ ->
                stringJoinIfNotEmpty " · " [ "", "two" ]
                    |> Expect.equal "two"
        , test "does not join last empty element" <|
            \_ ->
                stringJoinIfNotEmpty " · " [ "one", "" ]
                    |> Expect.equal "one"
        ]
