from typing import List
from re import findall, IGNORECASE, MULTILINE
from Repo import Repo
from SPARQLWrapper import SPARQLWrapper, POST, DIGEST, BASIC
from urllib.error import HTTPError
from uuid import uuid3, NAMESPACE_DNS

class Prefix():
    def __init__(self, key, url) -> None:
        self.key = key
        self.url = url
    
    def to_sparql_syntax(self):
        return f"PREFIX {self.key}: <{self.url}>"
    
    def __str__(self) -> str:
        return self.to_sparql_syntax()
    
    def __repr__(self) -> str:
        return self.to_sparql_syntax()



def import_resources_prefixes(path) -> List[Prefix]:
    with open(path, mode="r", encoding="UTF-8") as file:
        data = file.read()
    
    re_prefixes = r'^(\(add-prefix )"(\S*)" "(\S*)"(\))'

    matches = findall(re_prefixes, data, IGNORECASE | MULTILINE)
    prefixes = []
    for match in matches:
        prefixes.append(Prefix(match[1], match[2]))

    return prefixes


def add_repos_to_triplestore(repos: List[Repo]):
    prefixes = import_resources_prefixes("config/resources/repository.lisp")
    
    prefixes.append(Prefix("mu", "http://mu.semte.ch/vocabularies/core/"))

    sparql = SPARQLWrapper("http://localhost:8890/sparql")
    sparql.setHTTPAuth(BASIC)
    sparql.setCredentials("dba", "dba")
    sparql.setMethod("POST")
    

    sparql.addDefaultGraph("http://info.mu.semte.ch/microservices/")

    query = ""

    for prefix in prefixes:
        query += prefix.to_sparql_syntax() + "\n"
    
    query += "\nINSERT DATA {\n"
    
    for repo in repos:
        
        query += """
            GRAPH <http://mu.semte.ch/application> {{
                <http://info.mu.semte.ch/microservices/{uuid}> a ext:Microservice;
                mu:uuid "{uuid}";
                dct:title "{title}";
                dct:description "{description}";
                ext:repository "{repourl}";
                ext:isCoreMicroservice {isCore}.

            }}
            """.format(
                uuid=uuid3(NAMESPACE_DNS, repo.name),
                title=repo.name,
                description=repo.description,
                repourl=repo.repo_url,
                isCore="true" if repo.category.id == "core" else "false"
                
                
            )
    query += "}"

    print(query)

    sparql.setQuery(query)
    try:
        exec = sparql.query()
        print (exec.info())
    except HTTPError as e:
        print(e)

