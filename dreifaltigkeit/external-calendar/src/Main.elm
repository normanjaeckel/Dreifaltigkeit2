port module Main exposing (..)

import Browser
import Html exposing (Html, blockquote, br, dd, div, dl, dt, img, p, span, text)
import Html.Attributes exposing (alt, class, src, title)
import Http
import Iso8601
import Json.Decode as D
import Json.Decode.Pipeline as DP
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


externalCalendarUrl : Page -> String
externalCalendarUrl page =
    let
        url : String
        url =
            "https://kalender.evlks.de/json?vid=98"
    in
    case page of
        Home ->
            url ++ "&eventtype=1&itemsPerPage=1"

        Services ->
            url ++ "&eventtype=1"

        Calendar ->
            -- TODO: We can strip events in the past with "&start=2023-01-1&end=2999-12-25" which is useful with dynamic start value
            url ++ "&past=2"

        SingleEvent ->
            -- TODO: We can strip events in the past with "&start=2023-01-1&end=2999-12-25" which is useful with dynamic start value
            url ++ "&past=2"


localTimezome : Time.Zone
localTimezome =
    TimeZone.europe__berlin ()



-- MODEL


type alias Model =
    { flags : Maybe Flags
    , events : List Event
    }


init : E.Value -> ( Model, Cmd Msg )
init initialFlags =
    case initialFlags |> D.decodeValue flagsDecoder of
        Ok flags ->
            ( Model (Just flags) [], Http.get { url = externalCalendarUrl flags.page, expect = Http.expectJson GotEvents (D.list eventDecoder) } )

        Err _ ->
            ( Model Nothing [], Cmd.none )


type alias Flags =
    { page : Page
    , staticPrefix : String
    , monthlyTexts : List MonthlyText
    , defaultImage : Image
    , eventId : Int
    }


type Page
    = Home
    | Services
    | Calendar
    | SingleEvent


flagsDecoder : D.Decoder Flags
flagsDecoder =
    D.map5 Flags
        (D.field "page" pageDecoder)
        (D.maybe (D.field "staticPrefix" D.string)
            |> D.andThen (Maybe.withDefault "" >> D.succeed)
        )
        (D.maybe (D.field "monthlyTexts" (D.list monthlyTextDecoder))
            |> D.andThen (Maybe.withDefault [] >> D.succeed)
        )
        (D.maybe (D.field "defaultImage" defaultImageDecoder) |> D.andThen (Maybe.withDefault (Image "" "") >> D.succeed))
        (D.maybe (D.field "eventId" D.int) |> D.andThen (Maybe.withDefault 0 >> D.succeed))


pageDecoder : D.Decoder Page
pageDecoder =
    D.string
        |> D.andThen
            (\v ->
                case v of
                    "home-parish" ->
                        D.succeed Home

                    "services" ->
                        D.succeed Services

                    "calendar" ->
                        D.succeed Calendar

                    "singleEvent" ->
                        D.succeed SingleEvent

                    _ ->
                        D.fail "bad value for flag 'page'"
            )


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


defaultImageDecoder : D.Decoder Image
defaultImageDecoder =
    D.map2 Image
        (D.field "src" D.string)
        (D.field "text" D.string)


eventDecoder : D.Decoder Event
eventDecoder =
    D.field "Veranstaltung"
        (D.succeed Event
            |> DP.required "_event_EVENTTYPE" eventtypeDecoder
            |> DP.required "ID" (D.string |> D.andThen (String.toInt >> Maybe.withDefault 0 >> D.succeed))
            |> DP.required "_event_TITLE" D.string
            |> DP.required "SUBTITLE" D.string
            |> DP.required "_event_LONG_DESCRIPTION" D.string
            |> DP.required "START_RFC" Iso8601.decoder
            |> DP.required "END_RFC" Iso8601.decoder
            |> DP.required "LITURG_BEZ" D.string
            |> DP.required "_place_NAME" D.string
            |> DP.required "_event_LINK" D.string
            |> D.andThen
                (\fn ->
                    D.map2
                        (\src txt ->
                            if String.isEmpty src then
                                Nothing

                            else
                                Just <| Image src txt
                        )
                        (D.field "_event_IMAGE" D.string)
                        (D.field "_event_CAPTION" D.string)
                        |> D.andThen (\i -> fn i |> D.succeed)
                )
            |> DP.required "_event_MENUE_1" (D.string |> D.andThen (\v -> D.succeed <| v == "ja"))
        )



-- required : String -> Decoder a -> Decoder (a -> (b -> c)) -> Decoder (b -> c)


eventtypeDecoder : D.Decoder Eventtype
eventtypeDecoder =
    D.string
        |> D.andThen
            (\v ->
                case v of
                    "Gottesdienste" ->
                        D.succeed Service

                    "Gebete/Andachten/Friedensgebete" ->
                        D.succeed Prayer

                    "Konzerte/Theater/Musik" ->
                        D.succeed Concert

                    "Gruppen/Kreise" ->
                        D.succeed Gathering

                    "Freizeiten/Reisen" ->
                        D.succeed PeriodOfReflection

                    _ ->
                        D.succeed Miscellaneous
            )


eventEncoderForFullCalendar : Event -> E.Value
eventEncoderForFullCalendar event =
    let
        link =
            if String.isEmpty event.link then
                "/termine/" ++ String.fromInt event.id

            else
                event.link
    in
    E.object
        [ ( "title", E.string (stringJoinIfNotEmpty ": " [ event.title, event.liturgBez, event.subtitle ]) )
        , ( "start", E.string (event.start |> Iso8601.fromTime) )
        , ( "end", E.string (event.end |> Iso8601.fromTime) )
        , ( "color", E.string (event.eventtype |> eventtypeToColor) )
        , ( "url", E.string link )
        ]


type alias Event =
    { eventtype : Eventtype
    , id : Int
    , title : String
    , subtitle : String
    , longDescription : String
    , start : Time.Posix
    , end : Time.Posix
    , liturgBez : String
    , place : String
    , link : String
    , image : Maybe Image
    , withKidsService : Bool
    }


type Eventtype
    = Service
    | Prayer
    | Concert
    | Gathering
    | PeriodOfReflection
    | Miscellaneous


type alias MonthlyText =
    { month : MonthlyTextMonth
    , text : String
    , verse : String
    }


type alias MonthlyTextMonth =
    { year : Int
    , month : Time.Month
    }


type alias Image =
    { src : String
    , text : String
    }



-- UPDATE


type Msg
    = GotEvents (Result Http.Error (List Event))


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        GotEvents res ->
            case res of
                Err _ ->
                    ( model, Cmd.none )

                Ok events ->
                    ( { model | events = events }, eventsToJavascript (E.list eventEncoderForFullCalendar events) )


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
            case dataFromServer.page of
                Home ->
                    viewHome model

                Services ->
                    viewServices dataFromServer model

                Calendar ->
                    div [] []

                SingleEvent ->
                    viewSingleEvent dataFromServer model


viewHome : Model -> Html Msg
viewHome model =
    case model.events |> List.head of
        Nothing ->
            p [] [ text "Wann und wo wir den nächsten Gottesdienst in unserer Gemeinde feiern, erfahren Sie unter dem folgenden Link." ]

        Just service ->
            div []
                [ p [] [ text <| posixToStringWithWeekday service.start, br [] [], text service.place ]

                -- TODO: Linkify longDescription
                , p [] [ text <| stringJoinIfNotEmpty ": " [ service.liturgBez, service.title, service.subtitle, service.longDescription ] ]
                ]


viewServices : Flags -> Model -> Html Msg
viewServices dataFromServer model =
    let
        fn : Event -> ( List (Html Msg), Maybe MonthlyTextMonth ) -> ( List (Html Msg), Maybe MonthlyTextMonth )
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
    if List.isEmpty model.events then
        dl []
            [ dt [] [ text "Gottesdienste in der Trinitatiskirche oder der Markuskapelle" ]
            , dd [] [ text "Die nächsten Gottesdienste werden in Kürze bekannt gegeben." ]
            ]

    else
        dl []
            (model.events |> List.foldl fn ( [], Nothing ) |> Tuple.first)


monthlyTextFor : List MonthlyText -> MonthlyTextMonth -> List (Html Msg)
monthlyTextFor texts month =
    case texts |> List.filter (\mt -> mt.month == month) |> List.head of
        Just mt ->
            [ blockquote [] [ text mt.text, br [] [], text mt.verse ] ]

        Nothing ->
            []


serviceView : String -> Event -> List (Html Msg)
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
    [ dt [] [ text <| String.join " · " [ service.start |> posixToString, service.place, service.title ] ]
    , dd []
        (firstLine
            :: (if not <| String.isEmpty service.longDescription then
                    -- TODO: Linkify longDescription
                    [ p [] [ text service.longDescription ] ]

                else
                    []
               )
        )
    ]


viewSingleEvent : Flags -> Model -> Html Msg
viewSingleEvent flags model =
    case model.events |> List.filter (\e -> e.id == flags.eventId) |> List.head of
        Nothing ->
            div [] [ text "Veranstaltung nicht gefunden" ]

        Just event ->
            let
                ( imageSrc, imageText ) =
                    case event.image of
                        Just i ->
                            ( i.src, i.text )

                        Nothing ->
                            ( flags.staticPrefix ++ flags.defaultImage.src, flags.defaultImage.text )
            in
            div [ class "row" ]
                [ div [ class "6u", class "12u$(small)" ]
                    [ p [] [ text <| (event.start |> posixToString) ++ " · " ++ event.place ]
                    , p [] [ text <| stringJoinIfNotEmpty " · " [ event.title, event.subtitle ] ]

                    -- TODO: Linkify and Linebreaks for the longDescription
                    , p [] [ text event.longDescription ]
                    ]
                , div [ class "6u", class "12u$(small)" ]
                    [ span [ class "image", class "fit" ] [ img [ src imageSrc, alt imageText, title imageText ] [] ]
                    ]
                ]


posixToString : Time.Posix -> String
posixToString datetime =
    let
        day : String
        day =
            Time.toDay localTimezome datetime |> String.fromInt

        month : String
        month =
            Time.toMonth localTimezome datetime |> toGermanMonth

        year : String
        year =
            Time.toYear localTimezome datetime |> String.fromInt

        hour : String
        hour =
            Time.toHour localTimezome datetime |> String.fromInt |> withLeadingZero

        minute : String
        minute =
            Time.toMinute localTimezome datetime |> String.fromInt |> withLeadingZero

        withLeadingZero : String -> String
        withLeadingZero s =
            if String.length s < 2 then
                "0" ++ s

            else
                s
    in
    day ++ ". " ++ month ++ " " ++ year ++ " · " ++ hour ++ ":" ++ minute ++ " Uhr"


posixToStringWithWeekday : Time.Posix -> String
posixToStringWithWeekday datetime =
    (Time.toWeekday localTimezome datetime |> toGermanWeekday)
        ++ " · "
        ++ posixToString datetime


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


toGermanWeekday : Time.Weekday -> String
toGermanWeekday weekday =
    case weekday of
        Time.Mon ->
            "Montag"

        Time.Tue ->
            "Dienstag"

        Time.Wed ->
            "Mittwoch"

        Time.Thu ->
            "Donnerstag"

        Time.Fri ->
            "Freitag"

        Time.Sat ->
            "Sonnabend"

        Time.Sun ->
            "Sonntag"


stringJoinIfNotEmpty : String -> List String -> String
stringJoinIfNotEmpty sep chunks =
    chunks
        |> List.filter (not << String.isEmpty)
        |> String.join sep


eventtypeToColor : Eventtype -> String
eventtypeToColor et =
    case et of
        Service ->
            "darkorange"

        Prayer ->
            "red"

        Concert ->
            "green"

        Gathering ->
            "darkcyan"

        PeriodOfReflection ->
            "forestgreen"

        Miscellaneous ->
            "grey"



-- PORTS


port eventsToJavascript : E.Value -> Cmd msg
