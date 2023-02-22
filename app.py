from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_paginate import Pagination, get_page_parameter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATTIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nazva = db.Column(db.String(50), nullable=False)
    task_text = db.Column(db.String(100), nullable=False)
    answer = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Tasks %r>' % self.id


@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/posts')
def posts():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 5  # Количество постов на одной странице
    offset = (page - 1) * per_page
    articles = Article.query.order_by(Article.date.desc()).offset(offset).limit(per_page).all()
    total = Article.query.count()
    pagination = Pagination(page=page, total=total, per_page=per_page, css_framework='bootstrap4')
    return render_template('posts.html', articles=articles, pagination=pagination)

@app.route('/articles')
def show_articles():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 10 # Количество постов на одной странице
    offset = (page - 1) * per_page
    articles = Article.query.order_by(Article.date.desc()).offset(offset).limit(per_page).all()
    total = Article.query.count()
    pagination = Pagination(page=page, total=total, per_page=per_page, css_framework='bootstrap4')
    return render_template('articles.html', articles=articles, pagination=pagination)

@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/posts/<int:id>')
def post_detail(id):
    article = Article.query.get(id)
    return render_template('posts_detail.html', article=article)


@app.route('/posts/<int:id>/del')
def post_delete(id):
    article = Article.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return 'При видаленні сталася помилка'


@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']
        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return 'При додаванні виникла помилка'
    else:
        return render_template('create-article.html')


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    article = Article.query.get(id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']


        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return 'При редагуванны виникла помилка'
    else:
        return render_template('post_update.html', article=article)


@app.route('/create-tasks', methods=['POST', 'GET'])
def create_tasks():
    if request.method == 'POST':
        nazva = request.form['nazva']
        task_text = request.form['task_text']
        answer = request.form['answer']
        tasks = Tasks(nazva=nazva, task_text=task_text, answer=answer)

        try:
            db.session.add(tasks)
            db.session.commit()
            return redirect('/')
        except:
            return 'При додаванні виникла помилка'
    else:
        return render_template('create-tasks.html')


#
@app.route('/zadaniya/<int:id>')
def zadaniya_detail(id):
    tasks = Tasks.query.get(id)
    return render_template('zadaniya_detail.html', task=tasks)


@app.route('/zadaniya')
def zadaniya():
    tasks = Tasks.query.order_by(Tasks.date.desc()).all()
    return render_template('zadaniya.html', tasks=tasks)


@app.route('/blog/news')
def news():
    return render_template('news.html')


@app.route('/blog/id/news')
def news_id():
    return render_template('news_id.html')


@app.route('/admin-login/id')
def admin():
    return render_template('admin.html')


if __name__ == '__main__':
    app.run(debug=True)
