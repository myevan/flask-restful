# Flask-RESTful

[![Build Status](https://secure.travis-ci.org/twilio/flask-restful.png)](http://travis-ci.org/twilio/flask-restful)

Flask-RESTful provides the building blocks for creating a great REST API.

## New Features

### UTF8 JSON Representation

#### Code

    class HelloResource(Resource):
        def get(self):
            return {
                'hello' : u'안녕하세요',
            }
    
#### Old JSON Representation

    {
        'hello' : u'\uc548\ub155\ud558\uc138\uc694',
    }    

#### New JSON Representation

    {
        'hello' : '안녕하세요',
    }

#### Note

    

### API Routing Decorator

    @api.route('/')
    class HelloResource(Resource):
        def get(self):
            return {
                'hello' : 'world',
            }


    

## User Guide

You'll find the user guide and all documentation [here](http://flask-restful.readthedocs.org/en/latest/)

