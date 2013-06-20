# Flask-RESTful

[![Build Status](https://secure.travis-ci.org/twilio/flask-restful.png)](http://travis-ci.org/twilio/flask-restful)

Flask-RESTful provides the building blocks for creating a great REST API.

## New Features

### API Routing Decorator

    @api.route('/')
    class HelloResource(Resource):
        def get(self):
            return {
                'hello' : 'world',
            }

### UTF8 JSON Representation

#### Code

    class HelloResource(Resource):
        def get(self):
            return {
                'hello' : u'안녕하세요',
            }
    
#### Output

Old JSON Representation

    {
        'hello' : u'\uc548\ub155\ud558\uc138\uc694',
    }    

New JSON Representation

    {
        'hello' : '안녕하세요',
    }

#### Note

Old Representation Customizing

    @api.representation('application/xml')
    def xml(data, code, headers):
        resp = make_response(convert_data_to_xml(data), code)
        resp.headers.extend(headers)
        return resp
        
New Representation Customizing

    @api.representation('application/xml')
    def xml(data, code, headers):
        resp = make_response(convert_data_to_xml(data), code)
        resp.headers.extend(headers)

        resp.headers['Content-Type'] = 'application/xml; charset=utf-8'
        return resp
        

### API Error Representation

    @api.error_representation('application/json')
    def error_json(e):
        return output_json({
            'error' : repr(e),
            }, 500)    

## User Guide

You'll find the user guide and all documentation [here](http://flask-restful.readthedocs.org/en/latest/)

