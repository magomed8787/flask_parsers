from application import app


if __name__ == '__main__':
    print('Running server')
    app.run('localhost', 8080, False, threaded=False)
