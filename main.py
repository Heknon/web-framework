from web_framework import *


def main():
    server = HttpServer("webroot", "/index.html", "api")
    server.start()


if __name__ == '__main__':
    main()
