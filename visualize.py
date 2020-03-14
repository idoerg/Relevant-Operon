#!/usr/bin/env python
"""
Created on Wed Jul  6 16:14:23 2016

@author: huyn
@purpose: visualize professor John output
"""
from ete3 import *
import argparse
import os

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--Operon","-i", help="Operon file name")
    parser.add_argument("--Group","-g", help="Color Grouping")
    parser.add_argument("--Image","-o", help="Output Image")
    parser.add_argument("--Space","-s",help= "Space between the leaf node", default = 100)
    parser.add_argument("--Font","-f",help= "Font size", default = 50)
    parser.add_argument("--Branch","-b",help= "Branch thickness", default = 10000)
    parser.add_argument("--Tree","-t",help= "Tree file")
    args = parser.parse_args()
    return args
    
# color group of genome
# create a dictionary, sadly this is done manually
def parse(file):
    color_dic={}
    group= open(file,'r')
    for line in group.readlines():
        key= line.split(':')[0]
        color=line.split(':')[1]
        value = color.split('\n')[0]
        color_dic[key]=value
    return color_dic


if __name__ == "__main__":
    start = time.time()
    args = get_arguments()
    # branch thickness
    thickness = int(args.Branch)
    # parse the mapping file
    space   = int(args.Space)
    font    = int(args.Font)
    operon = args.Operon
    tree   = args.Tree
    # open the new convert file
    # get the mapping into dic
    infile = open(operon,'r')
    dic={}
    line = infile.readline()
    line = line.strip()
    line = line.split('\t')
    for item in line:
        item = item.split(',')
        dic[item[1]]=item[0]
    # get the gene block into another dic
    geneBlocks = {}
    for line in infile.readlines():
        line = line.strip()
        line = line.split(":")
        accession = line[0]
        block = line[1]
        geneBlocks[accession] = block
#    print (geneBlocks)
    color_list=['green','cyan','magenta','gray','yellow','orange',
               'red','lime','pink','blue','silver','maroon','mediumblue','plum']
    gene_color_dic = {}
    for gene in dic:
        color = color_list.pop(0)
        gene_color_dic[gene]= color
    tree= Tree(tree)
    # using the color dic to color group
    color_dic = parse(args.Group)
    far,distance = tree.get_farthest_leaf()
    for node in tree.iter_descendants("postorder"):
        if node.is_leaf():
            name = node.name.split('_')
            # modify name to be normal, and append the gene block info to it
            # get accesion number
            try:
                short = name[2]+'_'+name[3]
            except:
                short = name[-1]
            # get the color
            color = color_dic[short]
            node.add_features(node_color=color)
            # separate the node and the text
            gene_face = TextFace(" "*int(font/5))
            gene_face.background.color = "white"
            node.add_face(gene_face,0,"aligned")
            if "Bacillus_subtilis" in node.name or "Escherichia_coli" in node.name:
                node.name = name[0]+'_'+name[1]
                face =TextFace(node.name,fsize= font)
                face.margin_top =10
                face.margin_bottom = 10
                face.margin_left = 10
                face.margin_right = 20
                face.border.width = 10
                face.hz_align = 1
                face.vt_align = 1

                node.add_face(face, column =1,position ="aligned")
            else:
                node.name = name[0]+'_'+name[1]+"  "
                node.add_face(TextFace(node.name,fsize= font), column =1, position ="aligned")
                
            # retrieve the gene block
            try:
                genes = list(geneBlocks[short])
            except:
                genes = []
            # add a white column so it separate from the block
            col = 2
            gene_face = TextFace(" "*int(font/5))
            gene_face.background.color = "white"
            node.add_face(gene_face,col,"aligned")
            col = 3
            for gene in genes:
                if gene !="|":
                    gene_face = TextFace(gene,fsize= font)
                    gene_face.background.color = gene_color_dic[gene]                   
                else:
                    gene_face = TextFace(" "*int(font/5))
                    gene_face.background.color = "white"
                node.add_face(gene_face,col,"aligned")
                col+=1
                node.add_face(TextFace(" "),col,"aligned")
                col+=1

        nstyle = NodeStyle()
        # branch
        nstyle.hz_line_width = thickness
        nstyle.vt_line_width = thickness
        if node.is_leaf():
            nstyle["fgcolor"] = color
        else:
            nstyle["fgcolor"] = "gray"
        nstyle["shape"] = "circle"
        nstyle["size"] = font/2
        # nstyle["vt_line_color"]=color
        # nstyle["hz_line_color"]=color
        node.set_style(nstyle)
    ### get the total cost for each event:
    # get the 2 children of the tree
#    children= []
#    for child in tree.get_children():
#        children.append(child)
#    deletion_total = 0
#    duplication_total = 0
#    split_total = 0
#    for child in children:
#        deletion_total+= int(child.deletion.split('|')[1])
#        duplication_total+= int(child.duplication.split('|')[1])
#        split_total+= int(child.split.split('|')[1])
        
    # modify tree style for better visualization
    tree_style = TreeStyle()
    tree_style.branch_vertical_margin = space
    tree_style.show_leaf_name = False
    tree_style.min_leaf_separation = 5
    tree_style.extra_branch_line_type = 0
    tree_style.draw_guiding_lines=True
    tree_style.guiding_lines_type = 1
#    cost= TextFace("Deletion count: "+str(deletion_total)+
#                                '   '+"Duplication count: "+str(duplication_total)
#                                +'   '+"Split count: "+ str(split_total),fsize= font,penwidth=2)
#    cost.margin_top =5
#    cost.margin_bottom = 5
#    cost.margin_left = 40
#    cost.margin_right = 40
#    cost.border.width = 3
#    cost.border.color = "black"
#    tree_style.title.add_face(cost, column=1)
    mystring =''
    col = 1
    for gene in sorted(dic):
        color  = gene_color_dic[gene]      
        mystring = TextFace(gene+":"+dic[gene],fsize= font)
        mystring.margin_top =5
        mystring.margin_bottom = 5
        mystring.margin_left = 40
        mystring.margin_right = 40
        mystring.background.color = color
        tree_style.title.add_face(mystring, column=col)
        col+=1
    # render the image
#    tree.render(args.Image+'.pdf',dpi=1000,tree_style=tree_style)
    tree.render(args.Image+'.png',dpi=1000,tree_style=tree_style)
#    tree.render(args.Image+'.svg',dpi=1000,tree_style=tree_style)
#    tree.show(tree_style=tree_style)

