import flask
import yaml
import glob
from flask import Flask

app = Flask(__name__)

# create global plays dictionary
plays = {}
# loop over the files
for fn in glob.glob('data/*.yaml'):
    # load data from fn and put in dictionary
    with open(fn, 'r') as yf:
        play = yaml.load(yf)
        plays[play['id']] = play
print('done')

#///////////////////////////////////////////////////////////
#Some serious helper functions:

def getPreviousSceneObj(scene_pos, play):
    scenes = []
    # loop over the acts
    for act in play['acts']:
        # loop over the scenes
        for scene in act['scenes']:
            # add the scene to the master scenes list
            scenes.append(scene)
    print("IN MIDDLE")

    if (scene_pos > 0):
        return scenes[scene_pos - 1]
    else:
        return scenes[0]

def getNextSceneObj(scene_pos, play):
    scenes = []
    # loop over the acts
    for act in play['acts']:
        # loop over the scenes
        for scene in act['scenes']:
            # add the scene to the master scenes list
            scenes.append(scene)
    if (scene_pos == (len(scenes) - 1)):
        return scenes[scene_pos]
    else:
        return scenes[scene_pos + 1]

def getActForPrev(play, play_id, act_no, scene_no, scene_pos):
    print('hiGETACTPREV')
    prevSceneObj = getPreviousSceneObj(scene_pos, play)
    print(prevSceneObj)
    print(prevSceneObj.act)
    return prevSceneObj.act

def getSceneForPrev(play, play_id, act_no, scene_no, scene_pos):
    return getPreviousSceneObj(scene_pos, play).scene

def getPrevSceneName(play, play_id, act_no, scene_no, scene_pos):
    if ( getSceneForPrev(play, play_id, act_no, scene_no, scene_pos) == scene_no):
        return 'No Previous Scenes'
    else:
        return 'Act: ' + getActForPrev(play, play_id, act_no, scene_no) + 'Scene: ' + getSceneForPrev(play, play_id, act_no, scene_no)

def getActForNext(play, play_id, act_no, scene_no, scene_pos):
    return getNextSceneObj(scene_pos, play).act
def getSceneForNext(play, play_id, act_no, scene_no, scene_pos):
    return getNextSceneObj(scene_pos, play).scene

def getNextSceneName(play, play_id, act_no, scene_no, scene_pos):
    if ( getSceneForNext(play, play_id, act_no, scene_no) == scene_no):
        return 'No Next Scenes'
    else:
        return 'Act: ' + getActForNext(play, play_id, act_no, scene_no) + 'Scene: ' + getSceneForNext(play, play_id, act_no, scene_no)

#//////////////////////////////////////////////////////////
@app.route('/plays/<play_id>/')
def show_play(play_id):
    print(plays[play_id])
    return flask.render_template('IndividualPlay.html', play=plays[play_id])

@app.route('/plays/<play_id>/acts/<int:act_no>/scenes/<int:scene_no>')
def show_scene(play_id, act_no, scene_no): # show the scene!

    scenes = []
    # loop over the acts
    for act in play['acts']:
        # loop over the scenes
        for scene in act['scenes']:
            # add the scene to the master scenes list
            scenes.append(scene)
    #You can then search this scenes list for the scene you seek:
    scene = None
    scene_pos = None
    for i, s in enumerate(scenes):
        # check the act & scene number
        if s['act'] == act_no and s['scene'] == scene_no:
            scene = s
            scene_pos = i
            break

    #Previous: /acts/actForPrev/scenes/sceneForPrev: prevSceneName
    #Next: /acts/actForNext/scenes/sceneForNext: nextSceneName
    print('hi00')
    actForPrev = getActForPrev(plays[play_id], play_id, act_no, scene_no, scene_pos)
    print('hi01')
    sceneForPrev = getSceneForPrev(plays[play_id], play_id, act_no, scene_no, scene_pos)
    print('hi02')
    print(sceneForPrev)
    print(actForPrev)
    prevSceneName = getPrevSceneName(plays[play_id], play_id, act_no, scene_no, scene_pos)
    print('hi02.5')
    print(prevSceneName)
    print('hi03')
    actForNext = getActForNext(plays[play_id], play_id, act_no, scene_no, scene_pos)
    print('hi04')
    sceneForNext = getSceneForNext(plays[play_id], play_id, act_no, scene_no, scene_pos)
    print('hi05')
    nextSceneName = getNextSceneName(plays[play_id], play_id, act_no, scene_no, scene_pos)
    print('hi1')
    print(actForPrev + ' ' + sceneForPrev + ' ' + prevSceneName + ' ' + actForNext + ' ' + sceneForNext + ' ' + nextSceneName)
    print('hi2')
    return flask.render_template('IndividualScene.html',
                                 play=plays[play_id],
                                 act_no=act_no,
                                 scene_no=scene_no,
                                 actForPrev=actForPrev,
                                 sceneForPrev=sceneForPrev,
                                 prevSceneName=prevSceneName,
                                 actForNext=actForNext,
                                 sceneForNext=sceneForNext,
                                 nextSceneName=nextSceneName
                                )

@app.route('/')
def mainfunc():
    return flask.render_template('index.html', plays=plays) #, plays=yaml.load_all('/data/')
# , plays=yaml.load('/data/12night.yaml'



if __name__ == '__main__':
    app.run()
