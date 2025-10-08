import json
from graphviz import Graph

path = input("Enter JSON path : ")
with open(path, "r") as file:
    data = json.load(file)
    
ER = Graph(comment="ER Diagram", format="png")
ER.attr(splines="spline", bgcolor="white")

for entity in data["entities"]:
    entity_name = entity["name"].strip()
    ER.node(entity_name,entity_name, shape="box", style="filled", fillcolor="#d1e8ff")  #No two entites have same name so name = unique_id
   
    for attribute in entity["attributes"] :
        attribute_name = attribute["name"]
        attribute_id = f"{entity_name}+{attribute_name}"         #to uniquely identify each attribute by id = entity_name+attribute_name
        is_pk = attribute.get("isPrimaryKey", False)
        composite = attribute.get("composite", [])
        ismulti = attribute.get("isMultiValued", False)

        if is_pk:
            attribute_name =  f"<<u>{attribute_name}</u>>"     
            ER.node(attribute_id, attribute_name, shape="ellipse", fillcolor="#fff2cc", style="filled")
        elif ismulti:     
            ER.node(attribute_id, attribute_name, shape="ellipse", peripheries="2", fillcolor="#fff2cc", style="filled")
        else :
            ER.node(attribute_id, attribute_name, shape="ellipse", fillcolor="#fff2cc", style="filled")
            
        ER.edge(entity_name, attribute_id)
            

        for sub_attribute in composite :
            sub_attribute_id = f"{entity_name}+{attribute_name}+{sub_attribute}"
            ER.node(sub_attribute_id, sub_attribute, shape="ellipse", fillcolor="#f9daaf", style="filled")
            ER.edge(attribute_id, sub_attribute_id)


for relations in data["relationships"] :
    first_entity =  relations["entity1"]
    second_entity = relations["entity2"]
    relation_name = relations["name"] 
    cardinality = relations["cardinality"] 
    left_cardinality, right_cardinality = cardinality.split(":")

    ER.node(relation_name , relation_name , shape="diamond", style="filled", fillcolor="#f9bcbc") #No 2 relations have same name
    ER.edge(first_entity , relation_name , label = left_cardinality)
    ER.edge(relation_name , second_entity , label = right_cardinality)

    for attribute in relations.get("attributes", []):  #relationships can have attributes
        attribute_name = attribute["name"]
        attribute_id = f"{relation_name}+{attribute_name}"
        is_pk = attribute.get("isPrimaryKey", False)
        composite = attribute.get("composite", [])
        ismulti = attribute.get("isMultiValued", False)

        if is_pk:    
            ER.node(attribute_id, f"<u>{attribute_name}</u>", shape="ellipse", fillcolor="#fff2cc", style="filled")
        elif ismulti:     
            ER.node(attribute_id, attribute_name, shape="ellipse", peripheries="2",  fillcolor="#fff2cc", style="filled")
        else :
            ER.node(attribute_id, attribute_name, shape="ellipse", fillcolor="#fff2cc", style="filled")
            
        ER.edge(relation_name, attribute_id)

        for sub_attribute in composite :
            sub_attribute_id = f"{relation_name}+{attribute_name}+{sub_attribute}"
            ER.node(sub_attribute_id, sub_attribute, shape="ellipse", fillcolor="#f9daaf", style="filled")
            ER.edge(attribute_id, sub_attribute_id)

    


ER.render(filename="ER-diagram/ER Diagram", view=True, cleanup=True)
