module Main exposing (main)

import Browser
import Html exposing (Html, blockquote, br, dd, div, dl, dt, img, p, span, text)
import Html.Attributes exposing (alt, class, src, title)
import Http
import Iso8601
import Json.Decode as D
import Json.Encode as E
import Parser exposing ((|.), (|=))
import Time
import TimeZone


main : Program E.Value Model Msg
main =
    Browser.element
        { init = init
        , update = update
        , subscriptions = subscriptions
        , view = view
        }


externalCalendarUrl : String
externalCalendarUrl =
    "https://kalender.evlks.de/json?vid=98&eventtype=1"


localTimezome : Time.Zone
localTimezome =
    TimeZone.europe__berlin ()



-- MODEL


type alias Model =
    { flags : Maybe Flags
    , services : List Service
    }


init : E.Value -> ( Model, Cmd Msg )
init initialFlags =
    ( case initialFlags |> D.decodeValue flagsDecoder of
        Ok flags ->
            Model (Just flags) []

        Err _ ->
            Model Nothing []
    , Http.get { url = externalCalendarUrl, expect = Http.expectJson GotServices eventsDecoder }
    )


type alias Flags =
    { staticPrefix : String
    , monthlyTexts : List MonthlyText
    }


flagsDecoder : D.Decoder Flags
flagsDecoder =
    D.map2 Flags
        (D.field "staticPrefix" D.string)
        (D.field "monthlyTexts" (D.list monthlyTextDecoder))


monthlyTextDecoder : D.Decoder MonthlyText
monthlyTextDecoder =
    D.map3 MonthlyText
        (D.field "month" monthlyTextMonthDecoder)
        (D.field "text" D.string)
        (D.field "verse" D.string)


monthlyTextMonthDecoder : D.Decoder MonthlyTextMonth
monthlyTextMonthDecoder =
    let
        innerParser : Parser.Parser MonthlyTextMonth
        innerParser =
            Parser.succeed MonthlyTextMonth
                |= ((Parser.succeed ()
                        |. Parser.chompIf Char.isDigit
                        |. Parser.chompIf Char.isDigit
                        |. Parser.chompIf Char.isDigit
                        |. Parser.chompIf Char.isDigit
                    )
                        |> Parser.getChompedString
                        |> Parser.andThen
                            (\v ->
                                case v |> String.toInt of
                                    Just i ->
                                        Parser.succeed i

                                    Nothing ->
                                        Parser.problem "This problem should not be reachable."
                            )
                   )
                |= ((Parser.succeed ()
                        |. Parser.chompIf Char.isDigit
                        |. Parser.chompIf Char.isDigit
                    )
                        |> Parser.getChompedString
                        |> Parser.andThen
                            (\v ->
                                case v |> String.toInt of
                                    Just i ->
                                        case i of
                                            1 ->
                                                Parser.succeed Time.Jan

                                            2 ->
                                                Parser.succeed Time.Feb

                                            3 ->
                                                Parser.succeed Time.Mar

                                            4 ->
                                                Parser.succeed Time.Apr

                                            5 ->
                                                Parser.succeed Time.May

                                            6 ->
                                                Parser.succeed Time.Jun

                                            7 ->
                                                Parser.succeed Time.Jul

                                            8 ->
                                                Parser.succeed Time.Aug

                                            9 ->
                                                Parser.succeed Time.Sep

                                            10 ->
                                                Parser.succeed Time.Oct

                                            11 ->
                                                Parser.succeed Time.Nov

                                            12 ->
                                                Parser.succeed Time.Dec

                                            _ ->
                                                Parser.problem <| "Month " ++ String.fromInt i ++ " does not exist."

                                    Nothing ->
                                        Parser.problem "This problem should not be reachable."
                            )
                   )
    in
    D.int
        |> D.andThen
            (\m ->
                case m |> String.fromInt |> Parser.run innerParser of
                    Ok value ->
                        D.succeed value

                    Err _ ->
                        D.fail "Bad value for month in monthly text data."
            )


eventsDecoder : D.Decoder (List Service)
eventsDecoder =
    D.list <|
        D.field "Veranstaltung"
            (D.map7 Service
                (D.field "_event_TITLE" D.string)
                (D.field "SUBTITLE" D.string)
                (D.field "_event_LONG_DESCRIPTION" D.string)
                (D.field "START_RFC" Iso8601.decoder)
                (D.field "LITURG_BEZ" D.string)
                (D.field "_place_NAME" D.string)
                (D.field "_event_MENUE_1" D.string |> D.andThen (\v -> D.succeed <| v == "ja"))
            )


type alias Service =
    { title : String
    , subtitle : String
    , longDescription : String
    , start : Time.Posix
    , liturgBez : String
    , place : String
    , withKidsService : Bool
    }


type alias MonthlyText =
    { month : MonthlyTextMonth
    , text : String
    , verse : String
    }


type alias MonthlyTextMonth =
    { year : Int
    , month : Time.Month
    }



-- UPDATE


type Msg
    = GotServices (Result Http.Error (List Service))


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        GotServices res ->
            case res of
                Err _ ->
                    ( model, Cmd.none )

                Ok services ->
                    ( { model | services = services }, Cmd.none )


subscriptions : Model -> Sub Msg
subscriptions _ =
    Sub.none



-- VIEW


view : Model -> Html Msg
view model =
    case model.flags of
        Nothing ->
            div [] [ text "Interner Fehler" ]

        Just dataFromServer ->
            let
                fn : Service -> ( List (Html Msg), Maybe MonthlyTextMonth ) -> ( List (Html Msg), Maybe MonthlyTextMonth )
                fn service ( html, currentMonth ) =
                    let
                        thisMonth : MonthlyTextMonth
                        thisMonth =
                            MonthlyTextMonth (Time.toYear localTimezome service.start) (Time.toMonth localTimezome service.start)

                        printMonthlyText : List (Html Msg)
                        printMonthlyText =
                            case currentMonth of
                                Nothing ->
                                    monthlyTextFor dataFromServer.monthlyTexts thisMonth

                                Just month ->
                                    if month == thisMonth then
                                        []

                                    else
                                        monthlyTextFor dataFromServer.monthlyTexts thisMonth
                    in
                    ( html ++ printMonthlyText ++ serviceView dataFromServer.staticPrefix service, Just thisMonth )
            in
            dl []
                (model.services |> List.foldl fn ( [], Nothing ) |> Tuple.first)


monthlyTextFor : List MonthlyText -> MonthlyTextMonth -> List (Html Msg)
monthlyTextFor texts month =
    case texts |> List.filter (\mt -> mt.month == month) |> List.head of
        Just mt ->
            [ blockquote [] [ text mt.text, br [] [], text mt.verse ] ]

        Nothing ->
            []


serviceView : String -> Service -> List (Html Msg)
serviceView staticPrefix service =
    let
        firstLine : Html Msg
        firstLine =
            p []
                ((text <| stringJoinIfNotEmpty ": " [ service.liturgBez, service.subtitle ])
                    :: (if service.withKidsService then
                            [ span [ class "image", class "kids-logo", title "Kindergottesdienst" ]
                                [ img [ src <| staticPrefix ++ "images/Kindergottesdienst_Logo.jpg", alt "Kindergottesdienst" ] [] ]
                            ]

                        else
                            []
                       )
                )
    in
    [ dt [] [ text <| String.join " · " [ service.start |> startToString, service.place, service.title ] ]
    , dd []
        (firstLine
            :: (if service.longDescription /= "" then
                    [ p [] [ text service.longDescription ] ]

                else
                    []
               )
        )
    ]


startToString : Time.Posix -> String
startToString start =
    let
        day : String
        day =
            Time.toDay localTimezome start |> String.fromInt

        month : String
        month =
            Time.toMonth localTimezome start |> toGermanMonth

        year : String
        year =
            Time.toYear localTimezome start |> String.fromInt

        hour : String
        hour =
            Time.toHour localTimezome start |> String.fromInt |> withLeadingZero

        minute : String
        minute =
            Time.toMinute localTimezome start |> String.fromInt |> withLeadingZero

        withLeadingZero : String -> String
        withLeadingZero s =
            if String.length s < 2 then
                "0" ++ s

            else
                s
    in
    day ++ ". " ++ month ++ " " ++ year ++ " " ++ hour ++ ":" ++ minute ++ " Uhr"


toGermanMonth : Time.Month -> String
toGermanMonth month =
    case month of
        Time.Jan ->
            "Januar"

        Time.Feb ->
            "Februar"

        Time.Mar ->
            "März"

        Time.Apr ->
            "April"

        Time.May ->
            "Mai"

        Time.Jun ->
            "Juni"

        Time.Jul ->
            "Juli"

        Time.Aug ->
            "August"

        Time.Sep ->
            "September"

        Time.Oct ->
            "Oktober"

        Time.Nov ->
            "November"

        Time.Dec ->
            "Dezember"


stringJoinIfNotEmpty : String -> List String -> String
stringJoinIfNotEmpty sep chunks =
    case chunks of
        first :: rest ->
            if first == "" then
                stringJoinIfNotEmpty sep rest

            else if List.isEmpty rest then
                first

            else
                first ++ sep ++ stringJoinIfNotEmpty sep rest

        [] ->
            ""
