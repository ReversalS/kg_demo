import py2neo
import requests

from src.get_info import *

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    "Authorization": "token ff881363e6d18be63c6ae6de7d39a638facc5292"
}


def create_followers(node):
    """
    为参数结点在数据库中生成follower

    :param node: label为developer的结点
    :return:
    """

    info = {}

    try:
        info = requests.get(node["followers_url"], headers=headers).json()
    except KeyError:
        print("Node error")
        exit(-1)

    if info:
        followers = [member["url"] for member in info]
        for follower in followers:
            follower_info = requests.get(follower, headers=headers).json()
            properties, relationships = get_developer_info(follower_info)

            temp = properties.copy()
            temp.update(relationships)
            follower_node = py2neo.Node("DEVELOPER", **temp)
            rel1 = py2neo.Relationship(node, "IS_FOLLOWED_BY", follower_node)
            rel2 = py2neo.Relationship(follower_node, "FOLLOWS", node)
            tx.merge(follower_node, "DEVELOPER", "id")
            tx.create(rel1)
            tx.create(rel2)


if __name__ == '__main__':
    g = py2neo.Graph(
        host="localhost",
        http_port="7474",
        user="neo4j",
        password="123456"
    )

    tx = g.begin()

    matcher = g.nodes.match("DEVELOPER").where(
        "exists(()-[:IS_MADE_UP_OF]->(_)) and not exists((_)-[:IS_FOLLOWED_BY]->())")
    if len(matcher) != 0:
        n = matcher.first()
        create_followers(n)

    tx.commit()
