class Config():
    SECRET_KEY = 'inventarioflask129899'

class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = '129899'
    MYSQL_DB = 'inventarioflask'

config = {
    'development': DevelopmentConfig
}