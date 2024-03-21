import json
f=open('testplans.json')
data=json.load(f)
f.close()

for i in data['Testplan']['Features']:
    if('band' in data['Testplan']['Features'][i]):
        data['Testplan']['Features'][i]['estimated time']=0
        data['Testplan']['Features'][i]['Total']=0
        data['Testplan']['Features'][i]['band']['estimated time']=0
        data['Testplan']['Features'][i]['band']['Total']=0
        for j in data['Testplan']['Features'][i]['band']:
            if(j=='estimated time' or j=='Total'):
                continue
            if('security' in data['Testplan']['Features'][i]['band'][j]):
                data['Testplan']['Features'][i]['band'][j]['estimated time']=0
                data['Testplan']['Features'][i]['band'][j]['Total']=0
                data['Testplan']['Features'][i]['band'][j]['security']['estimated time']=0
                data['Testplan']['Features'][i]['band'][j]['security']['Total']=0
                for k in data['Testplan']['Features'][i]['band'][j]['security']:
                    if(k=='estimated time' or k=='Total'):
                        continue
                    if('channels' in data['Testplan']['Features'][i]['band'][j]['security'][k]):
                        data['Testplan']['Features'][i]['band'][j]['security'][k]['estimated time']=0
                        data['Testplan']['Features'][i]['band'][j]['security'][k]['Total']=0
                        data['Testplan']['Features'][i]['band'][j]['security'][k]['channels']['estimated time']=0
                        data['Testplan']['Features'][i]['band'][j]['security'][k]['channels']['Total']=0
                        for l in data['Testplan']['Features'][i]['band'][j]['security'][k]['channels']:
                            if(l=='estimated time' or l=='Total'):
                                continue
                            if('bandwidth' in data['Testplan']['Features'][i]['band'][j]['security'][k]['channels'][l]):
                                data['Testplan']['Features'][i]['band'][j]['security'][k]['channels'][l]['estimated time']=0
                                data['Testplan']['Features'][i]['band'][j]['security'][k]['channels'][l]['Total']=0
                                data['Testplan']['Features'][i]['band'][j]['security'][k]['channels'][l]['bandwidth']['estimated time']=0
                                data['Testplan']['Features'][i]['band'][j]['security'][k]['channels'][l]['bandwidth']['Total']=0
                                for m in data['Testplan']['Features'][i]['band'][j]['security'][k]['channels'][l]['bandwidth']:
                                    if(m=='estimated time' or m=='Total'):
                                        continue
                                    if('protocol' in data['Testplan']['Features'][i]['band'][j]['security'][k]['channels'][l]['bandwidth'][m]):
                                        data['Testplan']['Features'][i]['band'][j]['security'][k]['channels'][l]['bandwidth'][m]['estimated time']=0
                                        data['Testplan']['Features'][i]['band'][j]['security'][k]['channels'][l]['bandwidth'][m]['Total']=0
                                        data['Testplan']['Features'][i]['band'][j]['security'][k]['channels'][l]['bandwidth'][m]['protocol']['estimated time']=0
                                        data['Testplan']['Features'][i]['band'][j]['security'][k]['channels'][l]['bandwidth'][m]['protocol']['Total']=0
                                        for n in data['Testplan']['Features'][i]['band'][j]['security'][k]['channels'][l]['bandwidth'][m]['protocol']:
                                            if(n=='estimated time' or n=='Total'):
                                                continue
                                            if('sub_features' in data['Testplan']['Features'][i]['band'][j]['security'][k]['channels'][l]['bandwidth'][m]['protocol'][n]):
                                                data['Testplan']['Features'][i]['band'][j]['security'][k]['channels'][l]['bandwidth'][m]['protocol'][n]['estimated time'] = 0
                                                data['Testplan']['Features'][i]['band'][j]['security'][k]['channels'][l]['bandwidth'][m]['protocol'][n]['Total'] = 0
                                                data['Testplan']['Features'][i]['band'][j]['security'][k]['channels'][l]['bandwidth'][m]['protocol'][n]['sub_features']['estimated time'] = 0
                                                data['Testplan']['Features'][i]['band'][j]['security'][k]['channels'][l]['bandwidth'][m]['protocol'][n]['sub_features']['Total'] = 0
                                                for o in data['Testplan']['Features'][i]['band'][j]['security'][k]['channels'][l]['bandwidth'][m]['protocol'][n]['sub_features']:
                                                    if(o=='estimated time' or o=='Total'):
                                                        continue
                                                    data['Testplan']['Features'][i]['band'][j]['security'][k]['channels'][l]['bandwidth'][m]['protocol'][n]['sub_features'][o]['estimated time'] = 5
                                                    #replacing spaces with &nbsp;
                                                    data['Testplan']['Features'][i]['band'][j]['security'][k]['channels'][l]['bandwidth'][m]['protocol'][n]['sub_features'][o]['testcase name'] = data['Testplan']['Features'][i]['band'][j]['security'][k]['channels'][l]['bandwidth'][m]['protocol'][n]['sub_features'][o]['testcase name'].replace(' ','&nbsp;')
                                                    #adding number of testcases at each level
                                                    data['Testplan']['Features'][i]['band'][j]['security'][k]['channels'][l]['bandwidth'][m]['protocol'][n]['sub_features']['Total'] +=1
                                                    data['Testplan']['Features'][i]['band'][j]['security'][k]['channels'][l]['bandwidth'][m]['protocol'][n]['Total'] +=1
                                                    data['Testplan']['Features'][i]['band'][j]['security'][k]['channels'][l]['bandwidth'][m]['protocol']['Total'] +=1
                                                    data['Testplan']['Features'][i]['band'][j]['security'][k]['channels'][l]['bandwidth'][m]['Total'] +=1
                                                    data['Testplan']['Features'][i]['band'][j]['security'][k]['channels'][l]['bandwidth']['Total'] +=1
                                                    data['Testplan']['Features'][i]['band'][j]['security'][k]['channels'][l]['Total'] +=1
                                                    data['Testplan']['Features'][i]['band'][j]['security'][k]['channels']['Total'] +=1
                                                    data['Testplan']['Features'][i]['band'][j]['security'][k]['Total'] +=1
                                                    data['Testplan']['Features'][i]['band'][j]['security']['Total'] +=1
                                                    data['Testplan']['Features'][i]['band'][j]['Total'] +=1
                                                    data['Testplan']['Features'][i]['band']['Total'] +=1
                                                    data['Testplan']['Features'][i]['Total'] +=1
                                                    #adding estimated time at each level
                                                    data['Testplan']['Features'][i]['band'][j]['security'][k]['channels'][l]['bandwidth'][m]['protocol'][n]['sub_features']['estimated time'] += data['Testplan']['Features'][i]['band'][j]['security'][k]['channels'][l]['bandwidth'][m]['protocol'][n]['sub_features'][o]['estimated time']
                                                    data['Testplan']['Features'][i]['band'][j]['security'][k]['channels'][l]['bandwidth'][m]['protocol'][n]['estimated time'] += data['Testplan']['Features'][i]['band'][j]['security'][k]['channels'][l]['bandwidth'][m]['protocol'][n]['sub_features'][o]['estimated time']
                                                    data['Testplan']['Features'][i]['band'][j]['security'][k]['channels'][l]['bandwidth'][m]['protocol']['estimated time'] += data['Testplan']['Features'][i]['band'][j]['security'][k]['channels'][l]['bandwidth'][m]['protocol'][n]['sub_features'][o]['estimated time']
                                                    data['Testplan']['Features'][i]['band'][j]['security'][k]['channels'][l]['bandwidth'][m]['estimated time'] += data['Testplan']['Features'][i]['band'][j]['security'][k]['channels'][l]['bandwidth'][m]['protocol'][n]['sub_features'][o]['estimated time']
                                                    data['Testplan']['Features'][i]['band'][j]['security'][k]['channels'][l]['bandwidth']['estimated time'] += data['Testplan']['Features'][i]['band'][j]['security'][k]['channels'][l]['bandwidth'][m]['protocol'][n]['sub_features'][o]['estimated time']
                                                    data['Testplan']['Features'][i]['band'][j]['security'][k]['channels'][l]['estimated time'] += data['Testplan']['Features'][i]['band'][j]['security'][k]['channels'][l]['bandwidth'][m]['protocol'][n]['sub_features'][o]['estimated time']
                                                    data['Testplan']['Features'][i]['band'][j]['security'][k]['channels']['estimated time'] += data['Testplan']['Features'][i]['band'][j]['security'][k]['channels'][l]['bandwidth'][m]['protocol'][n]['sub_features'][o]['estimated time']
                                                    data['Testplan']['Features'][i]['band'][j]['security'][k]['estimated time'] += data['Testplan']['Features'][i]['band'][j]['security'][k]['channels'][l]['bandwidth'][m]['protocol'][n]['sub_features'][o]['estimated time']
                                                    data['Testplan']['Features'][i]['band'][j]['security']['estimated time'] += data['Testplan']['Features'][i]['band'][j]['security'][k]['channels'][l]['bandwidth'][m]['protocol'][n]['sub_features'][o]['estimated time']
                                                    data['Testplan']['Features'][i]['band'][j]['estimated time'] += data['Testplan']['Features'][i]['band'][j]['security'][k]['channels'][l]['bandwidth'][m]['protocol'][n]['sub_features'][o]['estimated time']
                                                    data['Testplan']['Features'][i]['band']['estimated time'] += data['Testplan']['Features'][i]['band'][j]['security'][k]['channels'][l]['bandwidth'][m]['protocol'][n]['sub_features'][o]['estimated time']
                                                    data['Testplan']['Features'][i]['estimated time'] += data['Testplan']['Features'][i]['band'][j]['security'][k]['channels'][l]['bandwidth'][m]['protocol'][n]['sub_features'][o]['estimated time']

f=open('testplans.json','w+')
json.dump(data,f,indent=4)
f.close()
