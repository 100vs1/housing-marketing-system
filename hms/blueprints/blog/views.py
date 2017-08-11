# -*- coding: utf-8 -*-
from flask import (
    Blueprint,
    redirect,
    request,
    flash,
    url_for,
    render_template)
from flask_login import (
    login_required,
    login_user,
    current_user,
    logout_user)
from sqlalchemy import text
from lib.util_json import render_json
from hms.blueprints.blog.forms import (
    SearchForm,
    PostForm
)
from hms.blueprints.blog.models import Post, Tag, Comment

blog = Blueprint('blog', __name__, template_folder='templates')


@blog.route('/posts', defaults={'page': 1})
@blog.route('/posts/page/<int:page>')
def posts(page):
    search_form = SearchForm()

    sort_by = Post.sort_by(request.args.get('sort', 'created_on'),
                           request.args.get('direction', 'desc'))
    order_values = '{0} {1}'.format(sort_by[0], sort_by[1])

    paginated_posts = Post.query \
        .filter(Post.search(request.args.get('q', ''))) \
        .order_by(text(order_values)) \
        .paginate(page, 50, True)

    return render_template('blog/index.html',
                           form=search_form,
                           posts=paginated_posts)


@blog.route('/posts/new', methods=['GET', 'POST'])
@login_required
def posts_new():
    form = PostForm()

    if form.validate_on_submit():
        post = Post()

        form.populate_obj(post)

        post.user_id = current_user.id

        post.save()

        flash('등록을 완료하였습니다.', 'success')
        return redirect(url_for('blog.posts'))

    return render_template('blog/new.html', form=form)


@blog.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def posts_edit(id):
    post = Post.query.get(id)
    form = PostForm(obj=post)

    if form.validate_on_submit() and post.user_id == current_user.id:
        form.populate_obj(post)

        post.user_id = current_user.id

        post.save()

        flash('수정을 완료하였습니다.', 'success')
        return redirect(url_for('blog.posts'))
    else:
        flash('본인이 등록한 글 외에는 수정할 수 없습니다.', 'error')

    return render_template('blog/edit.html', form=form, post=post)


@blog.route('/posts/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def posts_delete(id):
    post = Post.query.get(id)

    if post and post.user_id == current_user.id:
        post.delete()

        flash('삭제를 완료하였습니다.', 'success')
    else:
        flash('본인이 등록한 글 외에는 삭제할 수 없습니다.', 'error')

    return redirect(url_for('blog.posts'))


@blog.route('/tags', methods=['GET', 'POST'])
def tags():
    return render_json()