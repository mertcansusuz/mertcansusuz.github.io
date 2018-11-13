def create():
   import datetime
   db.forum_post.posted_by.default = auth.user.id
   db.forum_post.post_date.default = datetime.datetime.now() 
   form = crud.create(db.forum_post)  
   if form.process().accepted:
       session.flash = 'new blog post created'
       redirect(URL("forum","view", args=form.vars.id))
   return dict(form=form)

@auth.requires(auth.user_id==db.forum_post(request.args(0, cast=int)).posted_by
                or auth.has_membership(role="editor")
              )
def edit():
   post = db.forum_post(request.args(0, cast=int)) or redirect(URL('default','index'))
   form = crud.update("post", post.id, next=URL("view", args=post.id), 
                      message="post updated")
   return dict(post=post, form=form)

  
def view():
   post = db.forum_post(request.args(0, cast=int)) or redirect(URL('default','index'))
   post_author = db.auth_user(post.posted_by)   
   if auth.is_logged_in():   
       db.forum_comments.post_id.default = post.id
       db.forum_comments.posted_by.default = auth.user.id
       db.forum_comments.post_date.default = request.now
       form = crud.create(db.forum_comments)
       if form.process().accepted:
            response.flash = 'your comment is posted'
   else:
       form = None         
   comments = db(db.forum_comments.post_id == post.id).select()
   for comment in comments:
      author = db(db.auth_user.id == comment.posted_by).select()[0]
      comment.author = author.first_name + " " + author.last_name
   return dict(post=post, comments=comments,form=form, author=post_author)