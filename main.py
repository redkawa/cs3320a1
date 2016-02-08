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
    prevScene = int(format(scene_pos - 1))
    if (scene_pos > 0):
        return scenes[scene_pos - 1]
    else:
        return scenes[0]

def getActForPrev(play, play_id, act_no, scene_no, scene_pos):
    prevSceneObj = getPreviousSceneObj(scene_pos, play)
    return prevSceneObj['act']

def getSceneForPrev(play, play_id, act_no, scene_no, scene_pos):
    return getPreviousSceneObj(scene_pos, play)['scene']

def getPrevSceneName(play, play_id, act_no, scene_no, scene_pos):
    thePrevScene = getSceneForPrev(play, play_id, act_no, scene_no, scene_pos)
    thePrevAct = getActForPrev(play, play_id, act_no, scene_no, scene_pos)
    if ( thePrevScene == scene_no and
         thePrevAct == act_no):
        return 'No Previous Scene'
    else:
        print('else')
        return 'Act: {} Scene: {}'.format(thePrevAct, thePrevScene)

def getNextSceneObj(scene_pos, play):
    scenes = []
    # loop over the acts
    for act in play['acts']:
        # loop over the scenes
        for scene in act['scenes']:
            # add the scene to the master scenes list
            scenes.append(scene)
    scene_pos = int(format(scene_pos))
    if (scene_pos == (len(scenes) - 1)):
        return scenes[scene_pos]
    else:
        return scenes[scene_pos + 1]

def getActForNext(play, play_id, act_no, scene_no, scene_pos):
    return getNextSceneObj(scene_pos, play)['act']

def getSceneForNext(play, play_id, act_no, scene_no, scene_pos):
    return getNextSceneObj(scene_pos, play)['scene']

def getNextSceneName(play, play_id, act_no, scene_no, scene_pos):
    theNextScene = getSceneForNext(play, play_id, act_no, scene_no, scene_pos)
    theNextAct = getActForNext(play, play_id, act_no, scene_no, scene_pos)
    if ( theNextScene == scene_no and
         theNextAct == act_no):
        return 'No Next Scene'
    else:
        return 'Act: {} Scene: {}'.format(theNextAct, theNextScene)

#//////////////////////////////////////////////////////////
@app.route('/plays/<play_id>/')
def show_play(play_id):
    return flask.render_template('IndividualPlay.html', play=plays[play_id])

@app.route('/plays/<play_id>/acts/<int:act_no>/scenes/<int:scene_no>')
def show_scene(play_id, act_no, scene_no): # show the scene!
    scenes = []
    # loop over the acts
    for act in plays[play_id]['acts']:
        # loop over the scenes
        for scene in act['scenes']:
            # add the scene to the master scenes list
            scenes.append(scene)
    #You can then search this scenes list for the scene you seek:
    scene_pos = None
    for i, s in enumerate(scenes):
        # check the act & scene number
        if s['act'] == act_no and s['scene'] == scene_no:
            #scene = s
            scene_pos = i
            break

    scene_pos = int(format(scene_pos))
    #Previous: /acts/actForPrev/scenes/sceneForPrev: prevSceneName
    #Next: /acts/actForNext/scenes/sceneForNext: nextSceneName
    actForPrev = getActForPrev(plays[play_id], play_id, act_no, scene_no, scene_pos)
    sceneForPrev = getSceneForPrev(plays[play_id], play_id, act_no, scene_no, scene_pos)
    prevSceneName = getPrevSceneName(plays[play_id], play_id, act_no, scene_no, scene_pos)

    actForNext = getActForNext(plays[play_id], play_id, act_no, scene_no, scene_pos)
    sceneForNext = getSceneForNext(plays[play_id], play_id, act_no, scene_no, scene_pos)
    nextSceneName = getNextSceneName(plays[play_id], play_id, act_no, scene_no, scene_pos)

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
    return flask.render_template('index.html', plays=plays)

if __name__ == '__main__':
    app.run()
