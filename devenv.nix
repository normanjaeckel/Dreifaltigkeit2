# https://devenv.sh

{ pkgs, ... }:

{
  packages = [
    pkgs.go-task
    pkgs.elmPackages.elm-test
  ];

  languages.python = {
    enable = true;
    version = "3.11";
    venv.enable = true;
  };

  languages.elm.enable = true;

  enterShell = ''
    export LOCALE_ARCHIVE=/usr/lib/locale/locale-archive
  '';

  processes = {
    install-python-requirements.exec = "pip install --upgrade --requirement requirements.txt && pip freeze && sleep infinity";
  };

  env.PGUSER = "dreifaltigkeit";

  services.postgres = {
    enable = true;
    initialDatabases = [
      { name = "dreifaltigkeit_parish"; }
      { name = "dreifaltigkeit_kindergarden"; }
    ];
    initdbArgs = [ "--username=dreifaltigkeit" "--locale=C" "--encoding=UTF8" ];
  };
}
