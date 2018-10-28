def get_orgs_info(info):
    """
    处理组织的信息

    :param info: 字典，通过 GET: :orgs/org 获得
    :return: 两个列表，包含属性和关系
    """
    properties = {}
    relationships = {}
    properties_keys = ["id", "login", "description", "name", "company", "blog", "location", "email", "is_verified",
                       "has_organization_projects", "public_repos", "has_repository_projects",
                       "public_gists", "created_at", "updated_at"]
    relationships_keys = ["url", "hooks_url", "issues_url", "members_url", "public_members_url",
                          "repos_url", "events_url", "html_url"]

    if info:
        try:
            properties = {key: info[key] for key in properties_keys}
        except KeyError as ke:
            print(info)

        try:
            relationships = {key: info[key] for key in relationships_keys}
        except KeyError as ke:
            print(info)

        for key, value in relationships.items():
            try:
                value = value[:value.index("{")]
                relationships[key] = value
            except ValueError as ve:
                pass
    return properties, relationships


def get_developer_info(info):
    """
    处理开发者的信息

    :param info: 字典，通过 GET: :users/user 获得
    :return:两个列表，包含属性和关系
    """
    properties = {}
    relationships = {}
    properties_keys = ["id", "login", "name", "company", "blog", "location", "email", "hireable", "bio",
                       "public_repos",
                       "public_gists", "followers", "following", "created_at", "updated_at"]
    relationships_keys = ["url", "html_url", "followers_url", "following_url", "gists_url", "starred_url",
                          "subscriptions_url",
                          "organizations_url", "repos_url", "events_url", "received_events_url"]
    if info:
        properties = {key: info[key] for key in properties_keys}

        relationships = {key: info[key] for key in relationships_keys}

        for key, value in relationships.items():
            try:
                value = value[:value.index("{")]
                relationships[key] = value
            except ValueError as ve:
                pass

    return properties, relationships


def org_members(info):
    """
    处理组织的成员列表

    :param info: 字典
    :return: 返回包含成员url的列表
    """
    member_url = []
    if info:
        for member in info:
            member_url.append(member["url"])
    return member_url


def org_repos(info):
    """
    处理组织的仓库

    :param info: 字典
    :return: 两个列表，第一个包含字典(id，全名，url)，第二个包含所用到的语言
    """
    repo_info = []
    languages = []
    if info:
        for repo in info:
            temp = {"id": repo["id"], "full_name": repo["full_name"], "url": repo["url"], "language": repo["language"]}
            repo_info.append(temp)
            languages.append(repo["language"])
    return repo_info, languages
