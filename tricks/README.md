# git stuff

## pull changes from a fork 

(upstream=https://github.com/mechovation/40-VirtualRacing) to (local) master

```
(sds) rainer@neuron:~/dev/41-VirtualRacingRepos/40-VirtualRacing$ git remote
origin
(sds) rainer@neuron:~/dev/41-VirtualRacingRepos/40-VirtualRacing$ git remote add upstream https://github.com/mechovation/40-VirtualRacing.git
(sds) rainer@neuron:~/dev/41-VirtualRacingRepos/40-VirtualRacing$ git remote
origin
upstream
(sds) rainer@neuron:~/dev/41-VirtualRacingRepos/40-VirtualRacing$ git fetch upstream
From https://github.com/mechovation/40-VirtualRacing
 * [new branch]        master     -> upstream/master
(sds) rainer@neuron:~/dev/41-VirtualRacingRepos/40-VirtualRacing$ git checkout master
Already on 'master'
Your branch is up to date with 'origin/master'.
(sds) rainer@neuron:~/dev/41-VirtualRacingRepos/40-VirtualRacing$ git merge upstream/master
Updating 7234b91f..80dcc742
Fast-forward
 scripts/joydrive.py         | 146 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 training/README_20200421.md |   8 ++++
 2 files changed, 154 insertions(+)
 create mode 100644 scripts/joydrive.py
(sds) rainer@neuron:~/dev/41-(sds) rainer@neuron:~/dev/41-VirtualRacingRepos/40-VirtualRacing$ git push
```

## multiple repositories to push to
- https://stackoverflow.com/questions/11690709/can-a-project-have-multiple-origins#11690868

## update repo https://discordapp.com/channels/662098530411741184/694603353061195916/737554731295309864
```
cd ~/projects/donkeycar
git checkout master
git pull
cd ~/projects/gym-donkeycar
git checkout master
git pull
cd ~/mycar
donkey update
```

### add to myconfig.py
```
GYM_CONF["racer_name"] = "Your Name"
GYM_CONF["country"] = "USA"
GYM_CONF["bio"] = "I race robots."
```

## clone environment
```
conda create --name myclone --clone root
```
