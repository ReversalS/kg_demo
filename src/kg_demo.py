from collections import Counter

import py2neo
import requests

from src.get_info import *

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    "Authorization": "token 8403ca63eeb414e5239b23ed72076c3a3dd86680"
}
numpy_url = "https://api.github.com/orgs/numpy"

if __name__ == '__main__':

    # 初始化
    g = py2neo.Graph(
        host="localhost",
        http_port="7474",
        user="neo4j",
        password="123456"
    )

    g.delete_all()
    tx = g.begin()

    # 获取organization的属性/关系
    numpy_properties, numpy_relationships = get_orgs_info(requests.get(numpy_url, headers=headers).json())

    # 获取仓库的信息
    numpy_repos_info = requests.get(numpy_relationships["repos_url"], headers=headers).json()
    repos, language = org_repos(numpy_repos_info)

    # 获取仓库使用最多的属性
    numpy_properties["language"] = Counter(language).most_common()[0][0]

    # 建立numpy结点
    numpy_node = py2neo.Node("ORGANIZATION", **numpy_properties)
    tx.create(numpy_node)

    # 获取成员信息并建立结点
    numpy_members_info = requests.get(numpy_relationships["members_url"], headers=headers).json()
    member_urls = org_members(numpy_members_info)
    for url in member_urls:
        member_info = requests.get(url, headers=headers).json()
        properties, relationships = get_developer_info(member_info)
        member_node = py2neo.Node("DEVELOPER", **properties)
        tx.create(member_node)
        rel = py2neo.Relationship(numpy_node, "IS_MADE_UP_OF", member_node)
        tx.create(rel)

    # 建立仓库结点
    for repo in repos:
        repo_node = py2neo.Node("REPOSITORY", **repo)
        rel = py2neo.Relationship(numpy_node, "OWNS", repo_node)
        tx.create(repo_node)
        tx.create(rel)

    tx.commit()
