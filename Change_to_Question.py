
import httplib

def change_em(qid):
    conn = httplib.HTTPSConnection("gamesparks.freshdesk.com")
    rqid = str(qid)
    payload = "{\"type\":\"Question\"}"
    headers = {
        'authorization': "Basic T1JCeFFmdTd5MEM2TmdqcnBrRDoxMjM=",
        'content-type': "application/json",
        'cache-control': "no-cache",
        }
    
    conn.request("PUT", "/api/v2/tickets/"+rqid, payload, headers)
    
    res = conn.getresponse()
    data = res.read()

#     print(data.decode("utf-8"))





















