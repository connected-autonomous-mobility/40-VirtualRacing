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
