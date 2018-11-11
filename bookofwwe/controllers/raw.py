def raw_stars():
    raw_superstars = db().select(db.rawsuperstars.ALL, orderby=db.rawsuperstars.id)
    return dict(raw_superstars=raw_superstars)

def raw_star():
	raw_star = db.rawsuperstars(request.args(0, cast=int))
	if auth.is_logged_in():
		db.raw_comments.raw_id.default = raw_star.id
		db.raw_comments.posted_by.default = auth.user.id
		db.raw_comments.post_date.default = request.now
		form = crud.create(db.raw_comments)
		if form.process().accepted:
			response.flash = 'your comment is posted'
	else:
		form = None
	comments = db(db.raw_comments.raw_id == raw_star.id).select()
	for comment in comments:
		author = db(db.auth_user.id == comment.posted_by).select()[0]
		comment.author = author.first_name + " " + author.last_name
	return dict(raw_star=raw_star, comments=comments,form=form)



def raw_edit():
	star = db.rawsuperstars(request.args(0, cast=int)) or redirect(URL('default','index'))
	form = crud.update("rawsuperstars", star.id, next=URL("raw_star", args=star.id), message="star updated")
	return dict(star=star, form=form)

def raw_create():
	form = crud.create(db.rawsuperstars)  
	if form.process().accepted:
		session.flash = 'new blog post created'
		redirect(URL("raw","raw_star", args=form.vars.id))
	return dict(form=form)


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)