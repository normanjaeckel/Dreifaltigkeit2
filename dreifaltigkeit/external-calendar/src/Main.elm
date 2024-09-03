port module Main exposing (main, stringJoinIfNotEmpty)

import Browser
import Html exposing (Html, a, article, blockquote, br, dd, div, dl, dt, h1, h3, header, img, li, p, span, text, ul)
import Html.Attributes exposing (alt, class, href, src, title)
import Http
import Iso8601
import Json.Decode as D
import Json.Decode.Pipeline as DP
import Json.Encode as E
import Parser exposing ((|.), (|=))
import Shared
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
            url

        Services ->
            url ++ "&eventtype=1"

        Calendar ->
            -- TODO: We can strip events in the past with "&start=2023-01-1&end=2999-12-25" which is useful with dynamic start value
            url ++ "&past=2"

        SingleEvent ->
            -- TODO: We can strip events in the past with "&start=2023-01-1&end=2999-12-25" which is useful with dynamic start value
            -- TODO: Just fetch one single event here.
            url ++ "&past=2"


localTimezome : Time.Zone
localTimezome =
    TimeZone.europe__berlin ()


overrideLiturgBez : String -> String
overrideLiturgBez lbz =
    case lbz of
        "Drittl. Sonntag d. Kj." ->
            "Drittletzter Sonntag des Kirchenjahres"

        "Vorletzter Sonntag d. Kj." ->
            "Vorletzter Sonntag des Kirchenjahres"

        _ ->
            lbz



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
    , announcements : List Announcement
    , monthlyTexts : List MonthlyText
    , currentMarkusbote : CurrentMarkusbote
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
    D.map6 Flags
        (D.field "page" pageDecoder)
        (D.maybe (D.field "announcements" (D.list announcementDecoder))
            |> D.andThen (Maybe.withDefault [] >> D.succeed)
        )
        (D.maybe (D.field "monthlyTexts" (D.list monthlyTextDecoder))
            |> D.andThen (Maybe.withDefault [] >> D.succeed)
        )
        (D.maybe (D.field "currentMarkusbote" currentMarkusboteDecoder)
            |> D.andThen (Maybe.withDefault (CurrentMarkusbote "" "") >> D.succeed)
        )
        (D.maybe (D.field "defaultImage" imageDecoder) |> D.andThen (Maybe.withDefault (Image "" "") >> D.succeed))
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


announcementDecoder : D.Decoder Announcement
announcementDecoder =
    D.map5 Announcement
        (D.field "title" D.string)
        (D.field "short_text" D.string)
        (D.maybe (D.field "image" imageDecoder))
        (D.field "link" D.string)
        (D.field "end" Iso8601.decoder)


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


currentMarkusboteDecoder : D.Decoder CurrentMarkusbote
currentMarkusboteDecoder =
    D.map2 CurrentMarkusbote
        (D.field "url" D.string)
        (D.field "months" D.string)


imageDecoder : D.Decoder Image
imageDecoder =
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
            |> DP.optional "field30"
                (D.string
                    |> D.andThen
                        ((\v ->
                            if String.isEmpty v then
                                Nothing

                            else
                                Just v
                         )
                            >> D.succeed
                        )
                )
                Nothing
            |> DP.required "START_RFC" Iso8601.decoder
            |> DP.required "END_RFC" Iso8601.decoder
            |> DP.required "LITURG_BEZ" (D.string |> D.andThen (overrideLiturgBez >> D.succeed))
            |> DP.optional "field47"
                (D.string
                    |> D.andThen
                        ((\v ->
                            if String.isEmpty v then
                                Nothing

                            else
                                Just v
                         )
                            >> D.succeed
                        )
                )
                Nothing
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
            |> D.andThen
                (\fn ->
                    D.map2
                        (\src txt ->
                            src
                                |> Maybe.andThen
                                    (\s ->
                                        if String.isEmpty s then
                                            Nothing

                                        else
                                            Just <| Image s txt
                                    )
                        )
                        (D.maybe (D.field "field53" D.string))
                        (D.field "_event_CAPTION" D.string)
                        |> D.andThen (\i -> fn i |> D.succeed)
                )
            |> DP.required "_event_MENUE_1" (D.string |> D.andThen (\v -> D.succeed <| v == "mit Kindergottesdienst"))
        )


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
        link : String
        link =
            if String.isEmpty event.link then
                Shared.urls.events ++ String.fromInt event.id

            else
                event.link

        liturgBez : String
        liturgBez =
            case event.alternativeLiturgBez of
                Nothing ->
                    event.liturgBez

                Just lbz ->
                    lbz
    in
    E.object
        [ ( "title", E.string (stringJoinIfNotEmpty ": " [ event.title, liturgBez, event.subtitle ]) )
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
    , textOnHomePage : Maybe String
    , start : Time.Posix
    , end : Time.Posix
    , liturgBez : String
    , alternativeLiturgBez : Maybe String
    , place : String
    , link : String
    , image : Maybe Image
    , alternativeImage : Maybe Image
    , withKidsService : Bool
    }


type Eventtype
    = Service
    | Prayer
    | Concert
    | Gathering
    | PeriodOfReflection
    | Miscellaneous


type alias Announcement =
    { title : String
    , text : String
    , image : Maybe Image
    , link : String
    , end : Time.Posix
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


type alias CurrentMarkusbote =
    { url : String
    , month : String
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
                    viewHome dataFromServer model

                Services ->
                    viewServices dataFromServer model

                Calendar ->
                    div [] []

                SingleEvent ->
                    viewSingleEvent dataFromServer model


viewHome : Flags -> Model -> Html Msg
viewHome dataFromServer model =
    div [ class "posts" ]
        ((articleNextService model :: articleMarkusbote dataFromServer) ++ articleEventsAndAnnoucements dataFromServer model ++ [ articleAllEvents ])


articleNextService : Model -> Html Msg
articleNextService model =
    let
        imgLabel : String
        imgLabel =
            "Altar der Trinitatiskirche zu Leipzig Anger-Crottendorf mit Abendmahlsgeräten, Foto: Lutz Schober"
    in
    article []
        [ a [ href Shared.urls.services, class "image" ]
            [ img [ src <| Shared.staticPrefix ++ "images/Altar_02.jpg", title imgLabel, alt imgLabel ] []
            ]
        , h3 [] [ text "Nächster Gottesdienst" ]
        , case model.events |> List.filter (\e -> e.eventtype == Service) |> List.head of
            Nothing ->
                p [] [ text "Wann und wo wir den nächsten Gottesdienst in unserer Gemeinde feiern, erfahren Sie unter dem folgenden Link." ]

            Just service ->
                let
                    liturgBez : String
                    liturgBez =
                        case service.alternativeLiturgBez of
                            Nothing ->
                                service.liturgBez

                            Just lbz ->
                                lbz
                in
                div []
                    [ p [] [ text <| posixToStringWithWeekday service.start, br [] [], text service.place ]

                    -- TODO: Linkify longDescription
                    , p [] [ text <| stringJoinIfNotEmpty ": " [ liturgBez, service.title, service.subtitle, service.longDescription ] ]
                    ]
        , ul [ class "actions" ]
            [ li [] [ a [ href Shared.urls.services, class "button" ] [ text "Alle Gottesdienste" ] ]
            ]
        ]


articleMarkusbote : Flags -> List (Html Msg)
articleMarkusbote dataFromServer =
    if not <| String.isEmpty dataFromServer.currentMarkusbote.url then
        let
            imgLabel : String
            imgLabel =
                "Schriftzug des Markusboten, erste Ausgabe März 1907"
        in
        [ article []
            [ a [ href Shared.urls.markusbote, class "image" ]
                [ img [ src <| Shared.staticPrefix ++ "images/Markusbote_Schriftzug.jpg", title imgLabel, alt imgLabel ] []
                ]
            , h3 [] [ text "Aktueller Markusbote" ]
            , p []
                [ text "Hier finden Sie den aktuellen "
                , a [ href dataFromServer.currentMarkusbote.url ] [ text <| "Markusboten (Ausgabe " ++ dataFromServer.currentMarkusbote.month ++ ")" ]
                , text " als PDF zum Download."
                ]
            , ul [ class "actions" ]
                [ li [] [ a [ href Shared.urls.markusbote, class "button" ] [ text "Alle Markusboten" ] ]
                ]
            ]
        ]

    else
        []


type alias EventOrAnnouncement =
    { title : String
    , text : List String
    , image : Maybe Image
    , link : String
    , time : Int
    }


articleEventsAndAnnoucements : Flags -> Model -> List (Html Msg)
articleEventsAndAnnoucements dataFromServer model =
    let
        elements : List EventOrAnnouncement
        elements =
            let
                fn1 : Event -> List EventOrAnnouncement -> List EventOrAnnouncement
                fn1 event acc =
                    case event.textOnHomePage of
                        Just textOnHomePage ->
                            let
                                link : String
                                link =
                                    if String.isEmpty event.link then
                                        Shared.urls.events ++ String.fromInt event.id

                                    else
                                        event.link

                                image : Maybe Image
                                image =
                                    if event.alternativeImage == Nothing then
                                        event.image

                                    else
                                        event.alternativeImage
                            in
                            EventOrAnnouncement
                                event.title
                                [ posixToStringWithWeekday event.start, event.place, textOnHomePage ]
                                image
                                link
                                (event.start |> Time.posixToMillis)
                                :: acc

                        Nothing ->
                            acc

                fn2 : Announcement -> List EventOrAnnouncement -> List EventOrAnnouncement
                fn2 announcement acc =
                    EventOrAnnouncement
                        announcement.title
                        [ announcement.text ]
                        announcement.image
                        announcement.link
                        (announcement.end |> Time.posixToMillis)
                        :: acc
            in
            (model.events
                |> List.foldr fn1 []
            )
                ++ (dataFromServer.announcements |> List.foldr fn2 [])
    in
    elements
        |> List.sortBy (\el -> el.time)
        |> List.map
            (\el ->
                let
                    ( imageSrc, imageText ) =
                        case el.image of
                            Just i ->
                                ( i.src, i.text )

                            Nothing ->
                                ( Shared.staticPrefix ++ dataFromServer.defaultImage.src, dataFromServer.defaultImage.text )

                    paragraphs : List (Html Msg)
                    paragraphs =
                        el.text |> List.map (\t -> p [] [ text t ])
                in
                article []
                    ([ a [ href el.link, class "image" ] [ img [ src imageSrc, alt imageText, title imageText ] [] ]
                     , h3 [] [ text el.title ]
                     ]
                        ++ paragraphs
                        ++ [ ul [ class "actions" ] [ li [] [ a [ href el.link, class "button" ] [ text "Weitere Informationen" ] ] ]
                           ]
                    )
            )


articleAllEvents : Html Msg
articleAllEvents =
    let
        imgLabel : String
        imgLabel =
            "Kirchenschiff der Trinitatiskirche zu Leipzig Anger-Crottendorf, Foto: Lutz Schober"
    in
    article []
        [ a [ href Shared.urls.events, class "image" ]
            [ img [ src <| Shared.staticPrefix ++ "images/Trinitatiskirche_02.jpg", title imgLabel, alt imgLabel ] []
            ]
        , h3 [] [ text "Veranstaltungen im Überblick" ]
        , p [] [ text "Viele Termine und Veranstaltungen sind in unserem Kalender eingetragen." ]
        , ul [ class "actions" ]
            [ li [] [ a [ href Shared.urls.events, class "button" ] [ text "Zum Kalender" ] ]
            ]
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
            ( html ++ printMonthlyText ++ serviceView service, Just thisMonth )
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


serviceView : Event -> List (Html Msg)
serviceView service =
    let
        liturgBez : String
        liturgBez =
            case service.alternativeLiturgBez of
                Nothing ->
                    service.liturgBez

                Just lbz ->
                    lbz

        firstLine : Html Msg
        firstLine =
            p []
                ((text <| stringJoinIfNotEmpty ": " [ liturgBez, service.subtitle ])
                    :: (if service.withKidsService then
                            [ span [ class "image", class "kids-logo", title "Kindergottesdienst" ]
                                [ img [ src <| Shared.staticPrefix ++ "images/Kindergottesdienst_Logo.jpg", alt "Kindergottesdienst" ] [] ]
                            ]

                        else
                            []
                       )
                )
    in
    [ dt [] [ text <| String.join " · " [ service.start |> posixToString, service.place, service.title ] ]
    , dd []
        (firstLine :: (service.longDescription |> linebreaks))
    ]


viewSingleEvent : Flags -> Model -> Html Msg
viewSingleEvent flags model =
    case model.events |> List.filter (\e -> e.id == flags.eventId) |> List.head of
        Nothing ->
            header []
                [ h1 [] [ text "Veranstaltung nicht gefunden" ]
                ]

        Just event ->
            let
                ( imageSrc, imageText ) =
                    case event.alternativeImage of
                        Just i ->
                            ( i.src, i.text )

                        Nothing ->
                            case event.image of
                                Just i ->
                                    ( i.src, i.text )

                                Nothing ->
                                    ( Shared.staticPrefix ++ flags.defaultImage.src, flags.defaultImage.text )
            in
            div []
                [ header [ class "main" ]
                    [ h1 [] [ text event.title ]
                    ]
                , div [ class "row" ]
                    [ div [ class "6u", class "12u$(small)" ]
                        ([ p [] [ text <| (event.start |> posixToStringWithWeekday) ++ " · " ++ event.place ]
                         , p [] [ text event.subtitle ]
                         ]
                            -- TODO: Linkify long Descrition
                            ++ (event.longDescription |> linebreaks)
                        )
                    , div [ class "6u", class "12u$(small)" ]
                        [ span [ class "image", class "fit" ] [ img [ src imageSrc, alt imageText, title imageText ] [] ]
                        ]
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


linebreaks : String -> List (Html Msg)
linebreaks s =
    s
        |> String.split "\u{000D}\n\u{000D}\n"
        |> List.map (\part -> p [] [ text part ])



-- PORTS


port eventsToJavascript : E.Value -> Cmd msg
