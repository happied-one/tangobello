from bottle import get, redirect

from tangobello.models import BasketArticleList, Authors, Categories
from tangobello.serializers import post_serializer
from tangobello.utils import template
from tangobello.plugins import boilerplate_plugin


@get('/category/<category_name>', skip=[boilerplate_plugin])
@template('category.html')
def category(category_name):

    # get category information
    category_info = (Categories.get(Categories.category_name == category_name))

    # get posts list.
    article_list = (BasketArticleList.select().join(Authors, on=(Authors.author_id == BasketArticleList.author))
                    .where(BasketArticleList.category == category_info.category_id).order_by(BasketArticleList.post_date).limit(10))

    for post in article_list:
        post.category = category_info

    # get page number
    page_num = int(len(BasketArticleList.select(BasketArticleList.post_id)) / 10)
    #
    return {
        'article_list': post_serializer.dump(article_list, many=True).data,
        'current_page': 1,
        'max_page': page_num,
        'category': category_info
    }


@get('/category/<category_name>/page/<page:int>', skip=[boilerplate_plugin])
@template('category.html')
def category(category_name, page):
    if page == 1:
        redirect('/category/' + category_name)
    # get category information
    category_info = (Categories.get(Categories.category_name == category_name))

    # get posts list.
    article_list = (BasketArticleList.select().join(Authors, on=(Authors.author_id == BasketArticleList.author))
                    .where(BasketArticleList.category == category_info.category_id)
                    .order_by(BasketArticleList.post_date).paginate(page, 10))

    for post in article_list:
        post.category = category_info

    # get page number
    page_num = int(len(BasketArticleList.select(BasketArticleList.post_id)) / 10)
    #
    return {
        'article_list': post_serializer.dump(article_list, many=True).data,
        'current_page': page,
        'max_page': page_num,
        'category': category_info
    }
