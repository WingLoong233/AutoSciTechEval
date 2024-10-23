from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import FOAF, XSD
import json
import os

# 创建一个图
g = Graph()

# 定义命名空间
SCIKG = Namespace("https://www.aminer.cn/scikg/")
g.bind("scikg", SCIKG)

# 获取当前脚本所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 读取JSON数据
json_file_path = os.path.join(current_dir, 'SciKG_min_1.0.json')

# 使用分块读取来处理大文件
def process_json_in_chunks(file_path, chunk_size=1000):
    with open(file_path, 'r', encoding='utf-8') as file:
        decoder = json.JSONDecoder()
        buffer = ''
        for chunk in iter(lambda: file.read(chunk_size), ''):
            buffer += chunk
            while buffer:
                try:
                    result, index = decoder.raw_decode(buffer)
                    yield result
                    buffer = buffer[index:]
                except json.JSONDecodeError:
                    break

# 转换数据
for item in process_json_in_chunks(json_file_path):
    keyword_uri = URIRef(SCIKG[f"keyword/{item['id']}"])
    g.add((keyword_uri, RDF.type, SCIKG.Keyword))
    g.add((keyword_uri, SCIKG.name, Literal(item['name'])))
    g.add((keyword_uri, SCIKG.name_zh, Literal(item['name_zh'])))
    g.add((keyword_uri, SCIKG.level, Literal(item['level'], datatype=XSD.integer)))
    
    if 'definition' in item:
        g.add((keyword_uri, SCIKG.definition, Literal(item['definition'])))
    if 'definition_zh' in item:
        g.add((keyword_uri, SCIKG.definition_zh, Literal(item['definition_zh'])))
    
    if 'child_nodes' in item:
        for child_id in item['child_nodes']:
            child_uri = URIRef(SCIKG[f"keyword/{child_id}"])
            g.add((keyword_uri, SCIKG.hasChild, child_uri))
    
    if 'parent' in item:
        parent_uri = URIRef(SCIKG[f"keyword/{item['parent']}"])
        g.add((keyword_uri, SCIKG.hasParent, parent_uri))
    
    # 添加专家信息
    for expert in item.get('experts', []):
        expert_uri = URIRef(SCIKG[f"expert/{expert['id']}"])
        g.add((keyword_uri, SCIKG.hasExpert, expert_uri))
        g.add((expert_uri, RDF.type, SCIKG.Expert))
        g.add((expert_uri, FOAF.name, Literal(expert['name'])))
        if 'name_zh' in expert:
            g.add((expert_uri, SCIKG.name_zh, Literal(expert['name_zh'])))
        if 'position' in expert:
            g.add((expert_uri, SCIKG.position, Literal(expert['position'])))
        if 'affiliation' in expert:
            g.add((expert_uri, SCIKG.affiliation, Literal(expert['affiliation'])))
        g.add((expert_uri, SCIKG.h_index, Literal(expert['h_index'], datatype=XSD.integer)))
        for interest in expert.get('interests', []):
            g.add((expert_uri, SCIKG.hasInterest, Literal(interest)))

    # 添加出版物信息
    for pub in item.get('publications', []):
        pub_uri = URIRef(SCIKG[f"publication/{pub['id']}"])
        g.add((keyword_uri, SCIKG.hasPublication, pub_uri))
        g.add((pub_uri, RDF.type, SCIKG.Publication))
        g.add((pub_uri, SCIKG.title, Literal(pub['title'])))
        for author in pub.get('authors', []):
            author_uri = URIRef(SCIKG[f"author/{author['id']}"])
            g.add((pub_uri, SCIKG.hasAuthor, author_uri))
            g.add((author_uri, RDF.type, SCIKG.Author))
            g.add((author_uri, FOAF.name, Literal(author['name'])))

# 保存为Turtle格式
output_file_path = os.path.join(current_dir, "aminer_scikg.ttl")
g.serialize(destination=output_file_path, format="turtle")

print(f"转换完成。RDF数据已保存到：{output_file_path}")