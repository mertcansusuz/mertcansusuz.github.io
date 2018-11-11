def nxt_stars():
    nxt_superstars = db().select(db.nxtsuperstars.ALL, orderby=db.nxtsuperstars.id)
    return dict(nxt_superstars=nxt_superstars)

def nxt_star():
	nxt_star = db.nxtsuperstars(request.args(0, cast=int))
	if auth.is_logged_in():
		db.nxt_comments.nxt_id.default = nxt_star.id
		db.nxt_comments.posted_by.default = auth.user.id
		db.nxt_comments.post_date.default = request.now
		form = crud.create(db.nxt_comments)
		if form.process().accepted:
			response.flash = 'your comment is posted'
	else:
		form = None
	comments = db(db.nxt_comments.nxt_id == nxt_star.id).select()
	for comment in comments:
		author = db(db.auth_user.id == comment.posted_by).select()[0]
		comment.author = author.first_name + " " + author.last_name
	return dict(nxt_star=nxt_star, comments=comments,form=form)


def nxt_edit():
	star = db.nxtsuperstars(request.args(0, cast=int)) or redirect(URL('default','index'))
	form = crud.update("nxtsuperstars", star.id, next=URL("nxt_star", args=star.id), message="star updated")
	return dict(star=star, form=form)

def nxt_create():
	form = crud.create(db.nxtsuperstars)  
	if form.process().accepted:
		session.flash = 'new blog post created'
		redirect(URL("nxt","nxt_star", args=form.vars.id))
	return dict(form=form)


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)