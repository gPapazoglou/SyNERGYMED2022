import pandapower as pp
import pandas as pd

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


def transmission_network():
    net = pp.create_empty_network(name="Transmission Network")
    for i in range(3):
        pp.create_bus(net, 230)

    pp.create_gen(net, 0, 20, slack=True)
    pp.create_load(net, 1, 10)
    pp.create_load(net, 2, 5.7)

    f = [0, 0, 1]
    t = [1, 2, 2]

    for fb, tb in zip(f, t):
        pp.create_line_from_parameters(net, fb, tb, 1, 0, 1, 0, 0.5, max_loading_percent=100)

    net.flexibility = pd.DataFrame(columns=['bus', 'up_quantity', 'down_quantity', 'up_cost', 'down_cost'])
    net.flexibility['bus'] = [0, 1]
    net.flexibility['up_quantity'] = [5, 0]
    net.flexibility['down_quantity'] = [0, 1]
    net.flexibility['up_cost'] = [55, 0]
    net.flexibility['down_cost'] = [0, 50]

    return net

def distribution_network():
    net = pp.create_empty_network(name="Distribution Network")
    for i in range(3):
        #  bus mapping between net and paper: 0->4, 1->5, 2->6
        pp.create_bus(net, vn_kv=20, min_vm_pu=0.95, max_vm_pu=1.05)

    from_bus = [0, 1]
    to_bus = [1, 2]
    types = ['149-AL1/24-ST1A 10.0', '48-AL1/8-ST1A 10.0']

    for f, t, type in zip(from_bus, to_bus, types):
        pp.create_line(net, f, t, 1, std_type=type)

    net.line['max_i_ka'].loc[0] = 0.125

    pp.create_load(net, 1, p_mw=2.5, q_mvar=1)
    pp.create_load(net, 2, p_mw=1.8, q_mvar=0.8)

    net.flexibility = pd.DataFrame(columns=['bus', 'up_quantity', 'down_quantity', 'up_cost', 'down_cost'])
    net.flexibility['bus'] = [1, 2]
    net.flexibility['up_quantity'] = [1, 0]
    net.flexibility['down_quantity'] = [0, 0.1]
    net.flexibility['up_cost'] = [60, 0]
    net.flexibility['down_cost'] = [0, 50]

    # uncomment the 2 lines below if you need to run a power flow to identify
    # infeasibilities in the initial network state
    # pp.create_ext_grid(net, 0)
    # pp.runpp(net)

    return net

if __name__ == "__main__":
    tn = transmission_network()
    dn = distribution_network()

