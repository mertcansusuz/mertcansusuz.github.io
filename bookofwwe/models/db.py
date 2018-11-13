db = DAL("sqlite://storage.sqlite")


# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.14.1":
    raise HTTP(500, "Requires web2py 2.13.3 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# app configuration made easy. Look inside private/appconfig.ini
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
myconf = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(myconf.get('db.uri'),
             pool_size=myconf.get('db.pool_size'),
             migrate_enabled=myconf.get('db.migrate'),
             check_reserved=['all'])
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = ['*'] if request.is_local else []
# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = myconf.get('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.get('forms.separator') or ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

from gluon.tools import Auth, Service, PluginManager

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=myconf.get('host.names'))
service = Service()
plugins = PluginManager()

# -------------------------------------------------------------------------
# create all tables needed by auth if not custom tables
# -------------------------------------------------------------------------
auth.settings.extra_fields['auth_user']= [
  Field('address') ]
  
auth.define_tables(username=True, signature=False)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.get('smtp.server')
mail.settings.sender = myconf.get('smtp.sender')
mail.settings.login = myconf.get('smtp.login')
mail.settings.tls = myconf.get('smtp.tls') or False
mail.settings.ssl = myconf.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)





db.define_table('rawsuperstars',
                 Field("ring_name", required=True),
                 Field("real_name"),
                 Field("height"),
                 Field("weight"),
                 Field("hometown"),
                 Field("age"),
                 Field("achivements" , "text"),
                 Field("moves"),
                 Field("allies"),
                 Field("enemies"),
                 Field("cover" ,'upload'),
                 Field("video" , 'upload')
                 )

db.rawsuperstars.ring_name.required = True               
db.rawsuperstars.ring_name.required = IS_NOT_EMPTY()


db.define_table('sdsuperstars',
                 Field("ring_name", required=True),
                 Field("real_name"),
                 Field("height"),
                 Field("weight"),
                 Field("hometown"),
                 Field("age"),
                 Field("achivements" , "text"),
                 Field("moves"),
                 Field("allies"),
                 Field("enemies"),
                 Field("cover" , 'upload'),
                 Field("video" , 'upload')
                 )

db.sdsuperstars.ring_name.required = True               
db.sdsuperstars.ring_name.required = IS_NOT_EMPTY()



db.define_table('nxtsuperstars',
                 Field("ring_name", required=True),
                 Field("real_name"),
                 Field("height"),
                 Field("weight"),
                 Field("hometown"),
                 Field("age"),
                 Field("achivements" , "text"),
                 Field("moves"),
                 Field("allies"),
                 Field("enemies"),
                 Field("cover" , 'upload'),
                 Field("video" , 'upload')
                 )

db.nxtsuperstars.ring_name.required = True               
db.nxtsuperstars.ring_name.required = IS_NOT_EMPTY()


db.define_table('eventsDB',
                 Field("name", required=True),
                 Field("description" , "text"),
                 Field("cover"),
                 )

db.eventsDB.name.required = True               
db.eventsDB.name.required = IS_NOT_EMPTY()


post_cats = "News Forum".split()

db.define_table('post',
                Field('title'),
                Field('body', 'text'),                
                Field('posted_by', 'reference auth_user'),
                Field('post_date', 'datetime'),
                Field('category', 'list:string'),
                format = '%(title)s'
              )

db.define_table('comments',
                Field('body', 'text'),                
                Field('posted_by', 'reference auth_user'),
                Field('post_date', 'datetime'),
                Field('post_id', 'reference post'),
                format = '%(user)s comment on %(post_id)s'
              )
                              
db.post.category.requires=IS_IN_SET(post_cats) 
db.post.posted_by.requires = IS_IN_DB(db, db.auth_user.id)               
db.comments.posted_by.requires = IS_IN_DB(db, db.auth_user.id)
db.comments.post_id.requires = IS_IN_DB(db, db.post.id)

db.post.posted_by.writable = db.post.posted_by.readable = False
db.post.post_date.writable = db.post.post_date.readable = False
db.comments.post_id.writable = db.comments.post_id.readable = False
db.comments.post_date.writable = db.comments.post_date.readable = False
db.comments.posted_by.writable = db.comments.posted_by.readable = False

from gluon.tools import Crud
crud = Crud(db)



db.define_table('champsDB',
                Field("cover" , 'upload'),
                Field("championship"),
                Field("champion" , required=True),
                Field("defeated"),
                Field("date_won"),
                Field("which_event")
                )

db.champsDB.champion.required = True               
db.champsDB.champion.required = IS_NOT_EMPTY()



db.define_table('forum_post',
                Field('title'),
                Field('body', 'text'),                
                Field('posted_by', 'reference auth_user'),
                Field('post_date', 'datetime'),
                Field('category', 'list:string'),
                format = '%(title)s'
              )

db.define_table('forum_comments',
                Field('body', 'text'),                
                Field('posted_by', 'reference auth_user'),
                Field('post_date', 'datetime'),
                Field('post_id', 'reference post'),
                format = '%(user)s comment on %(post_id)s'
              )


db.forum_post.category.requires=IS_IN_SET(post_cats) 
db.forum_post.posted_by.requires = IS_IN_DB(db, db.auth_user.id)               
db.forum_comments.posted_by.requires = IS_IN_DB(db, db.auth_user.id)
db.forum_comments.post_id.requires = IS_IN_DB(db, db.forum_post.id)

db.forum_post.posted_by.writable = db.forum_post.posted_by.readable = False
db.forum_post.post_date.writable = db.forum_post.post_date.readable = False
db.forum_comments.post_id.writable = db.forum_comments.post_id.readable = False
db.forum_comments.post_date.writable = db.forum_comments.post_date.readable = False
db.forum_comments.posted_by.writable = db.forum_comments.posted_by.readable = False

from gluon.tools import Crud
crud = Crud(db)


db.define_table('nxt_comments',
                Field('body', 'text'),                
                Field('posted_by', 'reference auth_user'),
                Field('post_date', 'datetime'),
                Field('nxt_id', 'reference nxtsuperstars'),
                format = '%(user)s comment on %(nxt_id)s'
              )


db.nxt_comments.nxt_id.writable = db.nxt_comments.nxt_id.readable = False
db.nxt_comments.post_date.writable = db.nxt_comments.post_date.readable = False
db.nxt_comments.posted_by.writable = db.nxt_comments.posted_by.readable = False



db.define_table('sd_comments',
                Field('body', 'text'),                
                Field('posted_by', 'reference auth_user'),
                Field('post_date', 'datetime'),
                Field('sd_id', 'reference sdsuperstars'),
                format = '%(user)s comment on %(sd_id)s'
              )


db.sd_comments.sd_id.writable = db.sd_comments.sd_id.readable = False
db.sd_comments.post_date.writable = db.sd_comments.post_date.readable = False
db.sd_comments.posted_by.writable = db.sd_comments.posted_by.readable = False



db.define_table('raw_comments',
                Field('body', 'text'),                
                Field('posted_by', 'reference auth_user'),
                Field('post_date', 'datetime'),
                Field('raw_id', 'reference rawsuperstars'),
                format = '%(user)s comment on %(raw_id)s'
              )


db.raw_comments.raw_id.writable = db.raw_comments.raw_id.readable = False
db.raw_comments.post_date.writable = db.raw_comments.post_date.readable = False
db.raw_comments.posted_by.writable = db.raw_comments.posted_by.readable = False