### Multirtail
This utility watches logfiles and pipes the new lines to rtail (https://github.com/kilianc/rtail) stdin.

By default, it uses the name of the logfile for the stream-id.

### Setup
Copy `config-template.yml` to `config.yml` and edit `config.yml` in your favorite text editor.

### config.yml

```
multirtail:
    paths: <single/multiple file(s)/path(s)>
    debug: <False or True>
    showchanges: <False or True>
rtail:
    cmd: <path to the rtail-client>
    args: <any argument for rtail-client>
    host: <your rtail-server host>
```
