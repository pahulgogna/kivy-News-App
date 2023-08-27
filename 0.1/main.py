import requests as req  # for requesting API data
import webbrowser


from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.image import AsyncImage  # used to display images from the internet with there url
from kivy.uix.image import Image
from kivy.loader import Loader
# from kivy.uix.colorpicker import Color
# from kivy.core.window import Window

def GetResponse():
    return req.get(f'https://api.nytimes.com/svc/topstories/v2/science.json?api-key="YOUR API KEY"')

response = GetResponse()  # get the data from the new york times API

print('===',response,'===')

if response.json()['status'] == 'OK':
    print('Connection Successfull')

Article_number = response.json()['num_results']

def analyzeData(response_from_the_API):   # this function gives out a dictionary of news in an understandable format
    i = 0
    All_Data = response_from_the_API.json()['results']
    articles_Analyzed = {}
    for article in All_Data:
        i += 1
        articleNumber = f'article{i}'  # different each time through the loop
        url = article['url']
        published_date = article['published_date']
        title = article['title']
        # section = article['section']
        abstract = article['abstract']

        media = article['multimedia']

        if media != None:
            media_data = [dictionary['url'] for dictionary in media]
            
        else:
            media_data = []
        

        parsedData = {'title':title,  'url':url,  'abstract':abstract,  'published_date':published_date,  'media':media_data, 'all': media}  # creating a dictionary of this data for each article
        articles_Analyzed[articleNumber] = parsedData

    return articles_Analyzed

analyzed_Data = analyzeData(response)


Builder.load_string(''' 


<Scroll>:
    
    Grid:
        size_hint: 1, None
        height: self.minimum_height
    
<WrappedLabel>:
    size_hint_y: None
    text_size: self.width, None
    height: self.texture_size[1]


''')


class Scroll(ScrollView):
    def __init__(self, **kwargs):
        super(Scroll,self).__init__(**kwargs)

class imageformat(GridLayout):
    def horizontalLayout(self,i):
            imageURL = analyzed_Data[f'article{i+1}']['media']
            imgheight = analyzed_Data[f'article{i+1}']['all'][0]['height']
            print(imgheight)
        # this code is to change the image to a 'no image' when there is no image available in the article
            if imageURL != []:
                self.image = AsyncImage(source=imageURL[0],allow_stretch= True,size_hint= (1,None),height = imgheight)
                # self.image = Loader.image(imageURL[0])
                return self.image
            else:
                self.image = Image(source= 'images/NoImage.jpg')
                self.add_widget(self.image)
                return self.image
            

class urlManager:
    def urlOpener(self,url):
        webbrowser.open(str(url))
        # print(url)



class WrappedLabel(Label):
    def __init__(self, **kwargs):
        super(WrappedLabel, self).__init__(**kwargs)

class Grid(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.tiles()
    
    def urlOpener(self,url):
        webbrowser.open(str(url))
        print(url)

    def tiles(self):
        self.spacing = 80
        for i in range(Article_number):
            title = analyzed_Data[f'article{i+1}']['title']
            abstract = analyzed_Data[f'article{i+1}']['abstract']
            url = str(analyzed_Data[f'article{i+1}']['url'])
            self.heading = WrappedLabel(text= f"{title}",halign='center',bold= True)
            self.abstractLabel = WrappedLabel(text= abstract,halign='center')
            if title != '' :               
                self.add_widget(imageformat.horizontalLayout(self,i=i))
                self.add_widget(self.heading)
                self.add_widget(self.abstractLabel)
                if url == "null":
                    pass
                else:
                    self.urlLabel = WrappedLabel(text= f"[ref={url}]Source:[/ref]",halign='right',size_hint= (.5,1),height= 40,markup=True,padding_x= 20)
                    self.add_widget(self.urlLabel) #---------------------------------------------------------------------
                    self.urlLabel.bind(on_ref_press=lambda link, ref=url: self.urlOpener(ref))
            # self.add_widget(Label(text='', size_hint= (1,None),height= dp(5)))
        
            

    # def imageImporter(self,url):
    #     response = urllib.request.urlopen(url)
    #     imgArray = np.array(bytearray(response.read()), dtype=np.uint8)
    #     return cv2.imdecode(imgArray,1)
    
        
            
class MyNewsApp(App):  # building the app
    def build(self):
        # Window.clearcolor = (1,1,1,1)  # to change the color to white
        return Scroll()


if __name__ == '__main__':
    MyNewsApp().run()
