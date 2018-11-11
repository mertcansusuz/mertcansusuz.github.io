def sd_stars():
    sd_superstars = db().select(db.sdsuperstars.ALL, orderby=db.sdsuperstars.id)
    return dict(sd_superstars=sd_superstars)

def sd_star():
	sd_star = db.sdsuperstars(request.args(0, cast=int))
	if auth.is_logged_in():
		db.sd_comments.sd_id.default = sd_star.id
		db.sd_comments.posted_by.default = auth.user.id
		db.sd_comments.post_date.default = request.now
		form = crud.create(db.sd_comments)
		if form.process().accepted:
			response.flash = 'your comment is posted'
	else:
		form = None
	comments = db(db.sd_comments.sd_id == sd_star.id).select()
	for comment in comments:
		author = db(db.auth_user.id == comment.posted_by).select()[0]
		comment.author = author.first_name + " " + author.last_name
	return dict(sd_star=sd_star, comments=comments,form=form)

def sd_edit():
	star = db.sdsuperstars(request.args(0, cast=int)) or redirect(URL('default','index'))
	form = crud.update("sdsuperstars", star.id, next=URL("sd_star", args=star.id), message=" Smackdown Star Updated")
	return dict(star=star, form=form)

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)