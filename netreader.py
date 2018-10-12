# -*- coding: utf-8 -*-
import torch
from torchvision import models
from torchsummary import summary
from graphviz import Digraph
import torch
from torch.autograd import Variable


def make_dot(var, params=None):
    """ Produces Graphviz representation of PyTorch autograd graph
    Blue nodes are the Variables that require grad, orange are Tensors
    saved for backward in torch.autograd.Function
    Args:
        var: output Variable
        params: dict of (name, Variable) to add names to node that
            require grad (TODO: make optional)
    """
    print(var.grad_fn)
    if params is not None:
        assert isinstance(params.values()[0], Variable)
        param_map = {id(v): k for k, v in params.items()}
    

    node_attr = dict(style='filled',
                     shape='box',
                     align='left',
                     fontsize='12',
                     ranksep='0.1',
                     height='0.2')
    dot = Digraph(node_attr=node_attr, graph_attr=dict(size="12,12"))
    seen = set()

    def size_to_str(size):
        return '('+(', ').join(['%d' % v for v in size])+')'

    def add_nodes(var):
        
        if var not in seen:
            if torch.is_tensor(var):
                
                dot.node(str(id(var)), size_to_str(var.size()), fillcolor='orange')
            elif hasattr(var, 'variable'):
                
                u = var.variable
                #print(id(u),id(var))
                name = param_map[id(u)] if params is not None else ''
                node_name = '%s\n %s' % (name, size_to_str(u.size()))
                #print(u)
                dot.node(str(id(var)), node_name, fillcolor='lightblue')
            else:
                dot.node(str(id(var)), str(type(var).__name__))
            seen.add(var)
            if hasattr(var, 'next_functions'):
                
                for u in var.next_functions:
                    if u[0] is not None:
                        
                        dot.edge(str(id(u[0])), str(id(var)))
                        add_nodes(u[0])
            if hasattr(var, 'saved_tensors'):
                for t in var.saved_tensors:
                    
                    dot.edge(str(id(t)), str(id(var)))
                    add_nodes(t)
    add_nodes(var.grad_fn)
    return dot



def recursion(net_tuple):
    from torch.autograd import Variable


    i=0
    import re
    p1 = re.compile(r'[(](.*)[)]', re.S)
    #global i
    for n in net_tuple:
        #print(n)
        print(str(n).split("(")[0])
        try:
            recursion(n)
        except :
            print(re.findall(p1, str(n)))
            i+=1
#recursion(vgg)

    

#for i ,k in vgg.named_parameters():
    #print (i)
#g = make_dot(y)
#g.view()

#print(vgg)
    
#print(vgg)+


def outputsummary():
    """
    layer
    input_shape
    output_shape
    nb_params
    weight_shape
    
    """
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    vgg = models.AlexNet().to(device)
    #x = torch.randn(1,3,224,224).cuda()#change 12 to the channel number of network input

    #y = vgg(x)
    
    r_summary=summary(vgg, (3,3, 224, 224),batch_size=3)
    #for layer in r_summary:
        #print(r_summary[i]["input_shape"])
        #print(layer,r_summary[layer]['output_shape'],r_summary[layer]['nb_params'],)
    return r_summary




def make_OutputCubes(summary):

    for layer in summary:
        #print(summary[i]["input_shape"])
        #(layer,summary[layer]['output_shape'],summary[layer]['nb_params'],)
        
        if 'weight_shape' in summary[layer]:
            print(layer,summary[layer]['weight_shape'],summary[layer]['output_shape'])
            yield [3,summary[layer]['weight_shape'][-2],summary[layer]['weight_shape'][-1]]
        #else:
            #print(layer,False,summary[layer]['output_shape'])
        o_size=summary[layer]['output_shape']
        if len(o_size)==4:
            yield o_size[-3:]
        else :
            yield [2,o_size[-1]/10,o_size[-1]/10]

#summ=outputsummary()
#list(make_OutputCubes(summ))


#print(dict(vgg.named_parameters()).keys())










