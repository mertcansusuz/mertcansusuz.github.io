# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))


def news():
    cat  = request.args(0)
    posts = db(db.post.category == "News").select()
    for p in posts:
       author = db(db.auth_user.id == p.posted_by).select()[0]
       p.author = author
    return dict(category=cat, posts=posts)

def about():
    return dict()


def stars():
    return dict()


def star():
    return dict()
  

def champs():
    champions = db().select(db.champsDB.ALL, orderby=db.champsDB.id)
    return dict(champions=champions)


def forum():
    forum_posts = db(db.forum_post.category == "Forum").select()
    for p in forum_posts:
       author = db(db.auth_user.id == p.posted_by).select()[0]
       p.author = author
    return dict(forum_posts=forum_posts)
    


def events():
    events = db().select(db.eventsDB.ALL, orderby=db.eventsDB.id)
    return dict(events=events)

def event():
    event = db.eventsDB(request.args(0, cast=int))
    return dict(event=event)



def history():
    return dict()

    
def profile():
    username  = request.args(0)
    rows = db(db.auth_user.username == username).select()
    if len(rows) > 0:
       user = rows[0]
    else:
       user = None   
    return dict(user=user)

    



""" ___________ USER MANAGEMENT SYSTEM ____________________"""

@auth.requires_membership("editor") # uncomment to enable security 
def list_users():
    btn = lambda row: A("Edit", _href=URL('manage_user', args=row.auth_user.id))
    db.auth_user.edit = Field.Virtual(btn)
    rows = db(db.auth_user).select()
    headers = ["ID", "Name", "Last Name", "Email", "Edit"]
    fields = ['id', 'first_name', 'last_name', "email", "edit"]
    table = TABLE(THEAD(TR(*[B(header) for header in headers])),
                  TBODY(*[TR(*[TD(row[field]) for field in fields]) \
                        for row in rows]))
    table["_class"] = "table table-striped table-bordered table-condensed"
    return dict(table=table)



@auth.requires_membership("editor") # uncomment to enable security 
def manage_user():
    user_id = request.args(0) or redirect(URL('list_users'))
    form = SQLFORM(db.auth_user, user_id).process()
    membership_panel = LOAD(request.controller,
                            'manage_membership.html',
                             args=[user_id],
                             ajax=True)
    return dict(form=form,membership_panel=membership_panel)



@auth.requires_membership("editor") # uncomment to enable security 
def manage_membership():
    user_id = request.args(0) or redirect(URL('list_users'))
    db.auth_membership.user_id.default = int(user_id)
    db.auth_membership.user_id.writable = False
    form = SQLFORM.grid(db.auth_membership.user_id == user_id,
                       args=[user_id],
                       searchable=False,
                       deletable=False,
                       details=False,
                       selectable=False,
                       csv=False,
                       user_signature=False)
    return form


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


