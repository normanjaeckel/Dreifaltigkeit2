-- DO NOT EDIT: This is a generated file.


module Shared exposing (Urls, staticPrefix, urls)


staticPrefix : String
staticPrefix =
    "/static/"


type alias Urls =
    { services : String
    , markusbote : String
    , events : String
    }


urls : Urls
urls =
    Urls
        "/gottesdienste/"
        "/gemeinde/markusbote/"
        "/termine/"
