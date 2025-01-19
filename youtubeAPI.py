
from dateutil.relativedelta import relativedelta
from googleapiclient.discovery import build
import pandas as pd

from datetime import datetime



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
    #print(response["items"][0]["snippet"]["topLevelComment"]["etag"])
    #print(response["items"][0]["snippet"]["totalReplyCount"])
    #print(response["items"][0]["snippet"]["topLevelComment"])
    #print(response["items"][0]["snippet"]["topLevelComment"]["snippet"])


    service.close()

    #hp.PostID,         A
    #p.PlatformName,    A
    #hp.Timestamp,      A
    #spd.Username,      A
    #spd.PostContent,   A
    #spd.NumberOfComments,  A
    #spd.NumberOfLikes,     A
    # spd.URL,               A
    #spd.NumberOfReposts,   A   is anyway blank
    #spd.SearchedTopic      A
    comments=[]
    for item in response["items"]:
        timestamp = item["snippet"]["topLevelComment"]["snippet"]["publishedAt"]
        PostID=item["snippet"]["topLevelComment"]["etag"]
        Username = item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
        PostContent = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        NumberOfComments=item["snippet"]["totalReplyCount"]
        NumberOfReposts=None
        SearchedTopic=topic
        platformName="youtube"
        URL="https://www.youtube.com/watch?v=" + videoid
        NumberOfLikes = item["snippet"]["topLevelComment"]["snippet"]["likeCount"]
        #authorChannelUrl = item["snippet"]["topLevelComment"]["snippet"]["authorChannelUrl"]
        comments.append({"PostID":PostID,"Timestamp":timestamp,"PlatformName": platformName, "Username":Username,"PostContent": PostContent,"NumberOfComments":NumberOfComments,"NumberOfLikes": NumberOfLikes,"videoid":videoid,"SearchedTopic":SearchedTopic,"NumberOfReposts":NumberOfReposts,"URL":URL})
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

def getCommentDataMaster(topic,   start_date,   end_date,   number_of_data):
    #this funtion get comments from videos between start_date and end_date
    #each month we get a limited amount of videos. by doing this we get data that is evenly spread out over the months
    #from each of these videos we get a certain number of comments. pls note that some videos have comments deactivated


    #amount of month between the start and end
    temp= relativedelta(end_date,start_date)
    #print(temp.months)
    #amount of comments per video
    commentAmount =100


    #lower the numdata -> higher vid & lower comment
    #lower comment -> higher vid


    #amount of videos per month. PS you can only get at minimum 100 comments per month
    comMonth=number_of_data/temp.months
    vid_countMonth = 1/(1/comMonth / (1/commentAmount))
    if(vid_countMonth< 1):
        vid_countMonth=1


    dflist = []
    commentlist = pd.DataFrame()
    #iterate through months
    for i in range(0,temp.months):
        #get month videos. if we reach the api daily limit then it will stop
        print("here")
        try:
            df = getVideo(topic, vid_countMonth, start_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
                                     end_date.strftime("%Y-%m-%dT%H:%M:%SZ"), API_KEY=API_KEY[0])
            dflist.append(df)


        except:
            print("cant fetch anymore data (data limit) OR we are trying to get data from future")
            commentlist.to_csv("./data/comments/" + topic + "Entries" + str(commentlist.shape[0]) + ".csv", index=False)
            #print("here")
            return

        #this line of code is not really relavent
        dflist.append(df)
        
        #get X comments from each retrieved video
        for y in range(0, dflist[i].shape[0]):
            try:
                #get X comments from video y
                comdf = getCommentsThreadVideo(dflist[i].loc[y, "videoId"], commentAmount, API_KEY[1], topic)

                #add retireved comments to master dataframe
                commentlist = pd.concat([commentlist, comdf])

                # print(dflist[i].loc[y,"videoId"])
                # print(commentlist.shape[0])
            except:
                print("no comments for video: " + dflist[i].loc[y, "videoId"])

        #print(commentlist.shape[0])

        #go over to next month and repeat
        start_date = end_date
        end_date = start_date + relativedelta(months=1)
        print("here")
    #store dataframe as csv
    #commentlist.to_csv("./data/comments/" + topic +"Entries"+str(commentlist.shape[0])+ ".csv", index=False)
    return commentlist


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
    #getCommentsThreadVideo("Csau5f0TM8E",25,"AIzaSyBCTyv5uEZhMh8IJaWuMA_yegzxUonja1k")
    #getCommentsVideo("NPOHf20slZg")
    #print(getVideo("politics",2,"2024-01-01T00:00:01Z")["videoId"])
    start=datetime(2023,1,1)
    end=datetime(2023,2,1)
    df =getCommentDataMaster("Food",start,end,25)
    print(df)
    #Csau5f0TM8E
    #q-oSwyZ8NZw
    #videoCategorie()