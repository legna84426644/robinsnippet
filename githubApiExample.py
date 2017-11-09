'''
Created on Nov 11, 2017

@author: Robin

Get some information of Customer IO's github(https://github.com/customerio):
- How many total open issues are there across all repositories?
- Sort the repositories by date updated in descending order.
- Which repository has the most watchers?

'''
import requests, re
from datetime import datetime

baseURL = "https://api.github.com"
user = "customerio"
token = ""   # <--- input your token here
headers = {"Authorization": "token " + token}

def doGetRequest(url, headers):
    '''
    Do a get request for a url with a header and return the response
    '''
    try:
        print "do get request for: " + url
        r = requests.get(url, headers = headers)
    except Exception as e:
        print "Failed to do a get request with exception: " + str(e)
    return r

def iso8601ToSec(isoDate):
    '''
    Convert a iso 8601 timestamp into seconds (since Jan 1st 1970) 
    '''
    utc_dt = datetime.strptime(isoDate, '%Y-%m-%dT%H:%M:%SZ')
    timestamp = (utc_dt - datetime(1970, 1, 1)).total_seconds()
    return timestamp
    
def getPageNum(res):
    '''
    Get the number of response page of a request
    '''
    if 'Link' in res.headers:    
        link = res.headers['Link']
        lastLink = link.split(",")[1]
        s = re.findall("page=.*>; rel", lastLink)[0]
        s1 = s.split(">;")[0]
        pageNum = s1.split("page=")[1]
    else:
        pageNum = 1
    return pageNum

def getremainPage(url, pageMax):
    '''
    Get the remain items when the resouce has more than 30 items
    '''
    resourceList = []
    if "?" in url:
        pagePara = "&page="
    else:
        pagePara = "?page="
    page = 2
    while page <= pageMax:
        pageUrl = url + pagePara + str(page)
        r = doGetRequest(pageUrl, headers)
        res = r.json()
        resourceList = resourceList + res  
        page = page + 1
    return resourceList

def getPublicRepo(user):
    '''
    Get a list of repo for a user.
    '''
    url = baseURL + "/users/" + user + "/repos"
    r = doGetRequest(url, headers)
    res = r.json()
    repoList = res
    pageMax = int(getPageNum(r))
    if pageMax > 1:
        remainList = getremainPage(url, pageMax)
        repoList = repoList + remainList
    return repoList

def getWatchers(repo):
    '''
    Get a list of watchers for a repo
    '''
    url = baseURL + "/repos/" + user + "/" + repo + "/subscribers"
    r = doGetRequest(url, headers)
    res = r.json()
    watchers = res
    pageMax = int(getPageNum(r))
    if pageMax > 1:
        remainList = getremainPage(url, pageMax)
        watchers = watchers + remainList
    return watchers

def getIssues(repo):
    '''
    Get a list of issues for a repo
    '''
    url = baseURL + "/repos/" + user + "/" + repo + "/issues?state=open"
    r = doGetRequest(url, headers)
    res = r.json() 
    issues = res
    pageMax = int(getPageNum(r))
    if pageMax > 1:
        remainList = getremainPage(url, pageMax)
        issues = issues + remainList
    return issues

if __name__ == "__main__":
    # get all repos   
    repos = getPublicRepo(user)
    
    # make a list of repo name
    repoNameList = []
    for repo in repos:
        repoNameList.append(repo['name'])
        
    # make a dic of repo and update time
    repoUpdateDic = {}
    for repo in repos:
        name = repo['name']
        updateTime = repo['pushed_at']
        updateTimeSec = iso8601ToSec(updateTime)
        repoUpdateDic[name] = updateTimeSec
        repoNameList.append(name)
        
    # sort repoNameList by descending value
    repoSortedList = [] 
    for key, value in sorted(repoUpdateDic.iteritems(), key=lambda (k,v): (v,k), reverse=True):
        repoSortedList.append(key)
        
    # make a dic of repo and watcher
    repoWatchDic = {}
    (maxWatchers, repoMax) = (0, "") 
    for repo in repoNameList:
        watchers = getWatchers(repo)
        watcherNum = len(watchers)
        repoWatchDic[repo] = watcherNum
        if watcherNum > maxWatchers:
            maxWatchers = watcherNum
            repoMax = repo
              
    # make a dic of repo and issue
    repoIssueDic = {}
    issueTotal = 0
    for repo in repoNameList:
        issues = getIssues(repo)
        issueNum = len(issues)
        repoIssueDic[repo] = issueNum
        issueTotal = issueTotal + issueNum
    
    # do output
    print "Sort the repositories by date updated in descending order: " + str(repoSortedList)
    print "Repository has the most watchers is: " + repoMax
    print "Watcher number: " + str(maxWatchers)    
    print "Total open issues are there across all repositories: " + str(issueTotal)