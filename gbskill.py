import requests
import datetime

# parameters needed to access giantbomb api
mykey = "..."
base_url = "http://www.giantbomb.com/api/videos"
params = dict(
    api_key=mykey,
    field_list="name,publish_date",
    format="json",
    limit="1"
)
# giantbomb attempts to stop bots/scrapers by blocking ones that give a generic User-Agent in the header
# by specifiying the User-agent to something unique, we are able to circumvent this
headers = {
    'User-Agent': 'GiantBombSkill'
}

# this function is essential what gets called after app.run()
# the return value is what the alexa recieves and interprets
# there are a few formats to use I think, but json would propbably be the best
def lambda_handler(event, context):
    # requests info from giantbomb using the params from before
    resp = requests.get(url=base_url, params=params, headers=headers).json()
    # {u'number_of_page_results': 1, u'status_code': 1, u'error': u'OK', u'results': [{u'publish_date': u'2017-06-16 00:57:00', u'name': u'Giant Bomb at Nite - Live From E3 2017: Nite 3'}], u'version': u'1.0', u'limit': 1, u'offset': 0, u'number_of_total_results': 11734}
    # could add what date the video was added...
    date = resp['results'][0]['publish_date']
    speech_text = "The last video uploaded was %s" % resp['results'][0]['name']
    return create_json_response(speech_text)

def create_json_response(speech_text):
    # note that shouldEndSession is set to True as we are asking a single question, getting a single response
    # and then ending communication
    return {
        'version': "1.0",
        'response':
            {'outputSpeech':
                {'type': "PlainText",
                 'text': speech_text
                },
            'card':
                {'content': speech_text,
                'title': "Most Recent Video",
                'type': "Simple"
                },
            "reprompt":
                {'outputSpeech':
                    {'type':"PlainText",
                     'text': speech_text
                    }
                },
            'shouldEndSession': "True"
            },
            'sessionAttributes': {}
        }

if __name__ == '__main__':
    app.run()
