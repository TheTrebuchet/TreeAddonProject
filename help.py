mp_tosync = ['tps.Msides', 'tps.Mlength', 'tps.Mradius', 'tps.Mscale']
brp_tosync = ['tps.branch_levels', 'tps.branch_angle', 'tps.branch_height', 'tps.branch_variety', 'tps.branch_seed']
bn_tosync = ['tps.branch_number1', 'tps.branch_number2', 'tps.branch_number3']
bdp_tosync = ['tps.bends_amount', 'tps.bends_angle', 'tps.bends_correction', 'tps.bends_scale', 'tps.bends_weight', 'tps.bends_seed']
tp_tosync = ['tps.flare_amount', 'tps.branch_shift']
rp_tosync = ['tps.Rperlin_amount', 'tps.Rperlin_scale', 'tps.Rperlin_seed']

lists_tosync = [mp_tosync, brp_tosync, bn_tosync, bdp_tosync, tp_tosync, rp_tosync]
lists_source = ['m_p', 'br_p', 'bn_p', 'bd_p', 'r_p', 't_p']

for x in range(6):
    for i in range(len(lists_tosync[x])):
        print(lists_tosync[x][i] +' = '+lists_source[x]+'['+str(i)+']')