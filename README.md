### Multirtail
This utility watches logfiles and pipes the new lines to rtail stdin.

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
