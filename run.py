from patchserver import factory

application = factory.create_app()

if __name__ == "__main__":
    application.run(host="0.0.0.0", debug=True, threaded=True)
