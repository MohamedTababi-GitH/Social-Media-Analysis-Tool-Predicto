from dateutil.relativedelta import relativedelta
from googleapiclient.discovery import build
import pandas as pd
from spyder_kernels.utils.lazymodules import pandas
from tomlkit import datetime
import youtubeAPI
from numba.core.typing.builtins import Print
#pip install google-api-python-client

API_KEY=    ["AIzaSyBCTyv5uEZhMh8IJaWuMA_yegzxUonja1k",
            "AIzaSyBbfYbVAIMgz5mHfRErP-CIo1-m7M4vgUY",
            "AIzaSyBai_QALlQao-dY_A99mZq5LyQLSFKKRRg",
            "AIzaSyCg8JNIAbitjLkepytSFb702oC2zht1kUY",
            "AIzaSyC7F7K5UadtQk2eEh8EPGeE0thCkK2K4GY",
            "AIzaSyANaZogDET_Ovs_TNn6WFZRt6-o7ubFHZc",
            "AIzaSyDfyW4vs5a-juTQ5kVNpQmyI_pbsm8OInY",
            "AIzaSyC1Vren4zr71p9e6-wmFPXcHRcKT5YgXeE",
            "AIzaSyA8QQIa264DR0K9RII9DX7YDKyFhArSLEE",
            "AIzaSyC_olAirZQx3TXXgdxUZpQ4DSlj4xgTs-4"]

def getCommentsThreadVideo(videoid,amount,API_KEY,topic):

    #API_KEY = "AIzaSyBCTyv5uEZhMh8IJaWuMA_yegzxUonja1k"
    #API_SERVICE_NAME = 'youtubereporting';API_VERSION = 'v1'
    API_SERVICE_NAME = 'youtube'; API_VERSION = 'v3'
    #API_SERVICE_NAME = 'youtubeAnalytics'; API_VERSION = 'v2'


    service = build(API_SERVICE_NAME,API_VERSION,developerKey=API_KEY)


    #videoid = "NPOHf20slZg"
    part="snippet"
    response = service.commentThreads().list(
        part=part,
        videoId=videoid,
        textFormat = "plainText",
        maxResults=amount).execute()
    #print()
    #print(response)
    #print(response["items"][2]["snippet"]["topLevelComment"]["snippet"]["textDisplay"])
    #print(response["items"][1]["snippet"]["topLevelComment"]["snippet"])


    service.close()

    comments=[]
    for item in response["items"]:
        date = item["snippet"]["topLevelComment"]["snippet"]["publishedAt"]
        authorName = item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
        comment_text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        likes = item["snippet"]["topLevelComment"]["snippet"]["likeCount"]
        authorChannelUrl = item["snippet"]["topLevelComment"]["snippet"]["authorChannelUrl"]
        comments.append({"date":date,"authorName":authorName,"comment": comment_text,"num_of_likes": likes,"authorChannelUrl":authorChannelUrl,"videoid":videoid,"topic":topic})
    df = pd.DataFrame(comments)
    #print(df.iloc[0,:])
    return df

def getVideo(topic, amount,afterTime=None, beforeTime=None,API_KEY=None):

    #API_KEY = "AIzaSyBCTyv5uEZhMh8IJaWuMA_yegzxUonja1k"
    #API_SERVICE_NAME = 'youtubereporting';API_VERSION = 'v1'
    API_SERVICE_NAME = 'youtube'; API_VERSION = 'v3'
    #API_SERVICE_NAME = 'youtubeAnalytics'; API_VERSION = 'v2'


    service = build(API_SERVICE_NAME,API_VERSION,developerKey=API_KEY)



    #videoid = "NPOHf20slZg"
    part="snippet"
    #topic = "surfing"
    #amount=25

    response = service.search().list(
        part=part, channelId=None, channelType=None, eventType=None, forContentOwner=None, forDeveloper=None, forMine=None,
        location=None, locationRadius=None, maxResults=amount, onBehalfOfContentOwner=None, order=None, pageToken=None,
        publishedAfter=afterTime, publishedBefore=beforeTime, q=topic, regionCode=None, relevanceLanguage=None, safeSearch=None,
        topicId=None, type=None, videoCaption=None, videoCategoryId=None, videoDefinition=None, videoDimension=None,
        videoDuration=None, videoEmbeddable=None, videoLicense=None, videoPaidProductPlacement=None,
        videoSyndicated=None, videoType=None, x__xgafv=None).execute()


    service.close()
    #print()
    #print(response["items"])



    #print(response["items"][4])
    #print(response["items"][4]["id"].get("videoId"))
    #print(response["items"][4]["id"])

    videoData=[]
    for item in response["items"]:
        if item["id"].get("videoId") == None:
            continue
        videoId=item["id"]["videoId"]
        #print(videoId)
        date = item["snippet"]["publishedAt"]
        channelId=item["snippet"]["channelId"]
        channelTit= item["snippet"]["channelTitle"]
        title=item["snippet"]["title"]
        descrip=item["snippet"]["description"]

        videoData.append({"date":date,"videoId":videoId,"channelId": channelId,"channelTitle":channelTit,"title":title,"descrip":descrip,"topic":topic})
    df = pd.DataFrame(videoData)
    #print()
    #print(df.iloc[:,4])
    #print(df.to_json())
    return df

#use this simple method. will get x amount of videos and of those videos it will get y amount of comments each. 25 vid * 100 comments = about 25000 comments
#will get from a years worth of data
def getCommentDataMaster(topic,vidAmount,commentAmount,year,month,day):
    start = datetime(year, month, day)
    end = start + relativedelta(months=1)
    #print(start.strftime("%Y-%m-%dT%H:%M:%SZ"))
    #print(end.strftime("%Y-%m-%dT%H:%M:%SZ\n"))

    dflist=[]
    commentlist = pandas.DataFrame()
    for i in range(12):

        try:
            df = youtubeAPI.getVideo(topic, vidAmount, start.strftime("%Y-%m-%dT%H:%M:%SZ"),
                                 end.strftime("%Y-%m-%dT%H:%M:%SZ"), API_KEY=API_KEY[0])
            dflist.append(df)
        except:
            Print("cant fetch anymore data (data limit) OR we are trying to get data from future")
            commentlist.to_csv("./data/comments/" + topic +"Entries"+str(commentlist.shape[0])+ ".csv", index=False)
            return

        dflist.append(df)

        for y in range(0,dflist[i].shape[0]):
            try:
                #comdf=getCommentsThreadVideo(dflist[i].loc[y,"videoId"],100,API_KEY[1],"Food")
                #comdf.to_csv("./data/comments/Food/FoodComFile" + str(i + 1) +"Entrie"+str(y)+ ".csv", index=False)

                comdf=getCommentsThreadVideo(dflist[i].loc[y,"videoId"],commentAmount,API_KEY[1],topic)
                #comdf.to_csv("./data/comments/Politics/PolComFile" + str(i + 1) +"Entrie"+str(y)+ ".csv", index=False)
                commentlist=pd.concat([commentlist,comdf])

                #print(dflist[i].loc[y,"videoId"])
                #print(commentlist.shape[0])
            except:
                print("no comments for video: "+dflist[i].loc[y,"videoId"])


        print(commentlist.shape[0])



        start = end
        end = start + relativedelta(months=1)


    commentlist.to_csv("./data/comments/" + topic +"Entries"+str(commentlist.shape[0])+ ".csv", index=False)



#not finished. might get implemented later. was just messing around here
def videoCategorie():
    API_KEY = "AIzaSyBCTyv5uEZhMh8IJaWuMA_yegzxUonja1k"
    # API_SERVICE_NAME = 'youtubereporting';API_VERSION = 'v1'
    API_SERVICE_NAME = 'youtube';
    API_VERSION = 'v3'
    # API_SERVICE_NAME = 'youtubeAnalytics'; API_VERSION = 'v2'

    service = build(API_SERVICE_NAME, API_VERSION, developerKey=API_KEY)

    videoid = "NPOHf20slZg"
    part = "snippet"
    response = service.videoCategories().list(part=part, hl=None, id=None, regionCode=None, x__xgafv=None).execute()


    service.close()
    print(response)

    # comments=[]
    # for item in response["items"]:
    #    date = item["snippet"]["topLevelComment"]["snippet"]["publishedAt"]
    #    authorName = item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
    #    comment_text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
    #    likes = item["snippet"]["topLevelComment"]["snippet"]["likeCount"]
    #    authorChannelUrl = item["snippet"]["topLevelComment"]["snippet"]["authorChannelUrl"]
    #    comments.append({"date":date,"authorName":authorName,"comment": comment_text,"num_of_likes": likes,"authorChannelUrl":authorChannelUrl})
    # df = pd.DataFrame(comments)
    # print(df.iloc[0:5,:])



def test():
    getCommentsThreadVideo("Csau5f0TM8E",25,"AIzaSyBCTyv5uEZhMh8IJaWuMA_yegzxUonja1k")
    #getCommentsVideo("NPOHf20slZg")
    #print(getVideo("politics",2,"2024-01-01T00:00:01Z")["videoId"])

    #Csau5f0TM8E
    #q-oSwyZ8NZw
    #videoCategorie()