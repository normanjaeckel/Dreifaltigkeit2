module Main exposing (main)

import Browser
import Html exposing (blockquote, br, dd, dl, dt, img, p, span, text)
import Html.Attributes exposing (alt, class, src, title)
import Json.Decode as D
import Json.Encode as E


main : Program E.Value Model Msg
main =
    Browser.element
        { init = init
        , update = update
        , subscriptions = subscriptions
        , view = view
        }



-- MODEL


type alias Model =
    { flags : Flags }


init : E.Value -> ( Model, Cmd Msg )
init initialFlags =
    ( case initialFlags |> D.decodeValue flagsDecoder of
        Ok flags ->
            Model flags

        Err _ ->
            Model <| Flags "" ""
    , Cmd.none
    )


type alias Flags =
    { staticPrefix : String
    , monthlyTexts : String
    }


flagsDecoder : D.Decoder Flags
flagsDecoder =
    D.map2 Flags
        (D.field "staticPrefix" D.string)
        (D.field "monthlyTexts" D.string)



-- UPDATE


type Msg
    = Foo


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    ( model, Cmd.none )


subscriptions : Model -> Sub Msg
subscriptions _ =
    Sub.none



-- VIEW


view : Model -> Html.Html Msg
view model =
    dl []
        [ blockquote []
            [ text "Bibelvers hier"
            , br [] []
            , text "Bibelstelle"
            ]
        , dt [] [ text "5. November 2023 10:00 Uhr · Trinitatiskirche · Gottesdienst" ]
        , dd []
            [ p []
                [ text "22. Sonntag nach Trinitatis: Abendmahlsgottesdienst, anschließend Kirchenkaffee"
                , span [ class "image", class "kids-logo", title "Kindergottesdienst" ]
                    [ img [ src <| model.flags.staticPrefix ++ "images/Kindergottesdienst_Logo.jpg", alt "Kindergottesdienst" ] [] ]
                ]
            ]
        ]



-- ############### Previous code ###################
-- <dl>
--     {% for service in services %}
--     {% ifchanged %}
--     {% if service.monthly_text %}
--     <blockquote>{{ service.monthly_text.text }}<br />{{ service.monthly_text.verse }}</blockquote>
--     {% endif %}
--     {% endifchanged %}
--     <dt id="termin-{{ service.pk }}">{{ service.begin }} Uhr &middot; {{ service.place }} &middot;
--         {{service.get_type_display }}</dt>
--     <dd>
--         <p>
--             {{ service.title }}: {{ service.content|linkify }}
--             {% if service.for_kids %}
--             <span class="image kids-logo" title="Kindergottesdienst">
--                 <img src="{% static 'images/Kindergottesdienst_Logo.jpg' %}" alt="Kindergottesdienst" />
--             </span>
--             {% endif %}
--         </p>
--     </dd>
--     {% empty %}
--     <dt>Gottesdienste in der Trinitatiskirche oder der Markuskapelle</dt>
--     <dd>Die nächsten Gottesdienste werden in Kürze bekannt gegeben.</dd>
--     {% endfor %}
-- </dl>
