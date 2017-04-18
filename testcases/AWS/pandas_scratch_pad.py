#!/usr/bin/env python
import pandas as pd

job_manifests = [
    {"JobId": "1.0", "JOB_CPUS": 2, "JOB_MEM": 4, "JOB_MEM_UNITS": "GB"},
    {"JobId": "2.0", "JOB_CPUS": 2, "JOB_MEM": 4, "JOB_MEM_UNITS": "GB"},
    {"JobId": "3.0", "JOB_CPUS": 2, "JOB_MEM": 4, "JOB_MEM_UNITS": "GB"},
    {"JobId": "3.1", "JOB_CPUS": 2, "JOB_MEM": 4, "JOB_MEM_UNITS": "GB"},
    {"JobId": "3.2", "JOB_CPUS": 2, "JOB_MEM": 4, "JOB_MEM_UNITS": "GB"},
    {"JobId": "6.0", "JOB_CPUS": 2, "JOB_MEM": 4, "JOB_MEM_UNITS": "GB"}
]

resource_list = [
    {"RESOURCE_NAME": "AWS1", "RES_CPUS": 1, "RES_MEM": 2, "RES_MEM_UNITS": "GB"},
    {"RESOURCE_NAME": "AWS2", "RES_CPUS": 2, "RES_MEM": 4, "RES_MEM_UNITS": "GB"},
    {"RESOURCE_NAME": "AWS3", "RES_CPUS": 2, "RES_MEM": 6, "RES_MEM_UNITS": "GB"},
    {"RESOURCE_NAME": "AWS4", "RES_CPUS": 1, "RES_MEM": 6, "RES_MEM_UNITS": "GB"},
    {"RESOURCE_NAME": "AWS5", "RES_CPUS": 2, "RES_MEM": 5, "RES_MEM_UNITS": "GB"}
]

resource_spot_price = [
    {"RESOURCE_NAME": "AWS1", "SPOT_PRICE": .1},
    {"RESOURCE_NAME": "AWS2", "SPOT_PRICE": .15},
    {"RESOURCE_NAME": "AWS3", "SPOT_PRICE": .2},
    {"RESOURCE_NAME": "AWS4", "SPOT_PRICE": .12},
    {"RESOURCE_NAME": "AWS5", "SPOT_PRICE": .14}
]

def load_data_frame(list_of_dicts):
    list_of_keys = list_of_dicts[0].keys()
    pandas_data = {}
    for key in list_of_keys:
        pandas_data[key] = pd.Series([d[key] for d in list_of_dicts])
    return pd.DataFrame(pandas_data)

if __name__ == "__main__":
    # create jobs pandas data frame
    jobs_pd = load_data_frame(job_manifests)

    # create resources pandas data frame
    resources_pd = load_data_frame(resource_list)

    # create spot price pandas data frame
    spot_pd = load_data_frame(resource_spot_price)

    # merge the spot prices into the resources_pd
    resource_spot_pd = pd.merge(resources_pd, spot_pd, on=["RESOURCE_NAME"])

    # merge the two - sort of like:
    #   select *
    #   from jobs_pd, resources_pd
    #   where jobs_pd.JOB_CPUS <= resources_pd.RES_CPUS
    merged_pd = pd.merge(jobs_pd, resource_spot_pd, how='outer', left_on='JOB_CPUS', right_on='RES_CPUS')

    # create a new column that gives a boolean determining wether or not the row matches memory requirments
    merged_pd = merged_pd.assign(Match=merged_pd.JOB_MEM <= merged_pd.RES_MEM)

    # filter for matched entries in the data frame
    matched_pd = merged_pd[(merged_pd.Match == True)]
    number_of_jobs = len(matched_pd.index)

    group = matched_pd.groupby(['SPOT_PRICE','RESOURCE_NAME'])
    res_group = group['RESOURCE_NAME']

    req = {}
    limit = 5
    for i in res_group:
        entry_name = i[0][1]
        spot_price = i[0][0]

        print "considering jobs for %s" % entry_name
        print "number of jobs remaining: %i" % number_of_jobs
        print "limit: %i" % limit
        if number_of_jobs - limit > 0:
            req[entry_name] = (spot_price, limit)
            number_of_jobs -= limit
        elif number_of_jobs > 0:
            req[entry_name] = (spot_price, number_of_jobs)
            number_of_jobs = 0
        else:
            break
    print "number of unconsidered jobs: %i" % number_of_jobs

    for k in req.keys():
        print req[k]
