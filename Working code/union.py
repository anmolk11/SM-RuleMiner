cutoff = 0.5
def union(rules):
    """ Takes the rule set and returns its union """
    final_rule = {
        0 : [1e9,-1],
        3 : [1e9,-1],
        6 : [1e9,-1],
        9 : [1e9,-1],
        12 : [1e9,-1],
        15 : [1e9,-1],
        18 : [1e9,-1],
        21 : [1e9,-1]
    }

    for rule in rules:
        for i in range(0,len(rule),3):
            if(rule[i] >= cutoff):
                lb = min(rule[i + 1],rule[i + 2])
                ub = max(rule[i + 1],rule[i + 2])
                final_rule[i][0] = min(final_rule[i][0],lb)
                final_rule[i][1] = max(final_rule[i][0],ub)

    final_rule_vector = [i for i in range(24)]

    for k,v in final_rule.items():
        if(v[0] != 1e9 and v[1] != -1):
            final_rule_vector[k] = 1
            final_rule_vector[k + 1] = v[0]
            final_rule_vector[k + 2] = v[1]
        else:
            final_rule_vector[k] = 0
            final_rule_vector[k + 1] = 0
            final_rule_vector[k + 2] = 0
    return final_rule_vector

if __name__ == "__main__":
    rules = [
[0.0007846645471574487, 5.329496307360302, 5.140713072707239, 0.078530963327266, 15.706857882816657, 55.54264932057758, 0.4740644259356779, 122.0, 81.90230803075679, 0.3652960229466443, 29.791191860165924, 9.688096830483337, 0.7894938576243797, 681.7769779796482, 273.5501632845072, 0.17219150726572138, 0.0, 67.1, 0.2601193137643949, 0.078, 0.5942894855012146, 0.38748471314971367, 51.98134855150957, 40.67156729565979],

[0.0, 5.208445527754335, 8.940658800823515, 0.43495689778579527, 123.36647425054468, 94.86144383164479, 0.3111097735371558, 118.51422180858353, 111.40296007400688, 1.0, 95.48976953700337, 1.1971181985041053, 0.19420212915537494, 203.71267683456932, 735.8616715946062, 0.14450013530939065, 6.564151178664797, 46.96257406888425, 0.3425377514220539, 1.16247510359706, 2.1114926222054704, 0.8908700450258532, 40.042323384450825, 31.598973334054246],

[0.0014516118591746396, 11.871449982942496, 9.859810054675373, 0.8872605241951455, 19.28628056583461, 193.08820231175636, 0.25385197960867123, 90.55223689113376, 114.60076555222733, 0.6656914578718511, 15.035540281417541, 75.80612635663964, 0.29671113766795243, 0.10482340746891228, 434.98904277675797, 0.2965803177693924, 14.887804461830457, 38.55180291623033, 0.1151447681328095, 0.303896777958102, 1.2550424762112047, 0.3876838636171399, 47.06254815743452, 43.27064300422204],

[0.05796727129046686, 16.530970464834407, 0.50712567551654, 0.060150519725949536, 24.482384487392604, 181.36437939169681, 0.00887406144360392, 110.8223201038401, 100.95443616756896, 0.5014861398637369, 82.68393211807407, 19.70859307740177, 0.26846998901652863, 386.35634877980186, 575.474736960738, 0.011062418265505247, 9.673336747684363, 45.631240247744756, 0.1071912058791008, 0.876528075733114, 1.5130043745957578, 0.1899972689137731, 80.57237476595901, 75.96538707292345],

[0.8746751506693031, 3.302235801132094, 13.008113609758796, 0.05192857166099629, 175.6384802659949, 80.73988000760708, 0.28938119234838555, 95.72221574955489, 76.02105182168704, 0.4088884940644866, 44.6252903717102, 98.40296859974127, 0.4776345696236832, 563.6785848704756, 658.0072847735182, 0.01245867231459763, 34.1600430782728, 15.40761386662317, 0.4757934625746616, 1.4636382410758952, 1.4281061250134506, 0.4647634456946056, 39.14339855087512, 77.90094160107527],

[0.47128818613079304, 16.615330886983227, 16.863147304875096, 0.07995769186502155, 23.92034657248621, 179.73189850676746, 0.46776992705872356, 78.90285329135173, 8.629229580095837, 0.3068607638714539, 91.45153024021694, 33.78339592733045, 0.8134783769243369, 130.52735466565304, 796.1478870690996, 0.351928129304815, 59.85480495622248, 4.675261218682487, 0.04623753626717064, 1.9984597761726, 0.10736362040934083, 0.27260479008604366, 52.81396756924693, 61.1619943412967],

[0.7179756968602053, 3.3642026410222323, 17.0, 0.33369914959151337, 156.22904414180977, 18.649728998511257, 0.35148707334463014, 120.76100698946895, 72.91015109246428, 0.32836545081473845, 15.668453275592716, 86.70545183276454, 0.13093606405045477, 626.5031287849295, 430.47780701769847, 0.8703626280427852, 39.10496234736059, 5.280522773524648, 0.6620564189151122, 0.15575513894612164, 2.2012578293553764, 0.10326420254935287, 51.43357361778992, 49.73557405001472],

[0.4371980755791166, 13.68182797550448, 2.9167806049883502, 0.09676466810751638, 164.63490727241023, 28.434396104115525, 0.2684890519256601, 60.0148566179858, 7.525798608564051, 0.7770779637430067, 22.550233906499777, 72.22096662471823, 0.4609860244685049, 605.7994534333051, 399.32381048256696, 0.0036461176502924353, 34.057623788446755, 45.83835051854022, 0.43501714320451934, 0.42532338665934066, 1.1548905059806194, 0.7585434829150737, 23.941450389782872, 78.43490965549594],

[0.40384551172073635, 4.7966905367723305, 4.282716547297381, 0.17166793565312655, 164.06413628876933, 5.727758052393661, 0.25221951083832794, 117.1424897231521, 30.00866617109895, 0.3421047233724819, 16.979828735648773, 51.654344519828314, 0.9326001149458306, 154.61062133771247, 822.0174667785782, 0.48132913159181534, 56.11819650601242, 24.867862898715316, 0.2570771879243765, 2.1144928753561913, 0.9129436435045758, 0.3819960116575861, 45.592926015530644, 40.347294337490126],

[0.8766918568096227, 16.948082323780703, 6.101719173938852, 0.45382862288497494, 78.41571600075119, 55.87463200893333, 0.46042796169803113, 86.32752446465523, 56.43385811939692, 0.4289952810761184, 25.568777103480105, 94.8644664600134, 0.25802669961449265, 548.8062004519652, 791.8011159792829, 0.6225893793489075, 39.94221995589393, 0.0, 0.2658809511202972, 0.81093639823356, 2.130638330406136, 0.011653321805243033, 24.63633511629246, 75.32193149223258],

[0.029491905101029836, 10.664563331306013, 2.461205689570434, 0.22058298084915628, 36.32383532656174, 48.78223980594699, 0.3389768839380596, 69.660921802192, 56.6567071117071, 0.46308141160393756, 59.38992242193051, 92.7644764759403, 0.8697862067391122, 191.77109447105087, 583.0034491069338, 0.24123691850992446, 31.749732836266105, 54.34546436234096, 0.4940128454576168, 1.8688515159950565, 0.29599122205916856, 0.21715329763881208, 41.2913867686413, 44.88017504898213],

[0.4008409979770283, 15.444255603272218, 5.941737746198627, 0.37113767946717124, 10.629919921486827, 179.07860960223402, 0.1744234073292127, 22.191043350992373, 25.53263995892096, 0.2851757880273589, 45.50526580404967, 84.90821859852021, 0.8566544093587026, 86.13353505516443, 627.4479098074324, 0.4024292306158258, 37.03969151545802, 45.14081095586525, 0.38781567445239884, 1.8403132628867191, 0.7447942357866836, 0.7073323821381897, 30.447079150776545, 79.21926299450995],

[0.4182483915003401, 15.532560076762099, 11.18310816092057, 0.4667631478920714, 146.2980992242172, 87.57982366511176, 0.3414250224543638, 2.216357111493206, 45.94738433769973, 0.640574852317235, 37.83004740262129, 88.93321726837787, 0.4163922214616176, 42.5568916447631, 121.27317295262576, 0.28633034551467074, 22.449506907439783, 28.916815555032688, 0.4354486343501687, 0.9121777393973344, 1.5937221061454676, 0.3068602532230752, 73.42200604907669, 44.76365989789981],

[0.011686517578886724, 9.241010571230245, 10.994311399741909, 0.4237444589120981, 172.74589656091553, 46.15285173019154, 0.2402675251489631, 74.30675098488533, 67.13638982496698, 0.16762957130747458, 39.219091446064965, 37.03983592882147, 0.27755707686029785, 280.72309486773725, 785.4638304331872, 0.6490086983877535, 61.00937487445431, 9.034128074120554, 0.2216246995215274, 0.22584991620430828, 1.600059370195913, 0.5843480309434849, 30.444107880890947, 79.22739781099638]
]

final_rule = union(rules)
print(final_rule)