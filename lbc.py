from config.config import module_error_message

from threading import Thread    
from time import sleep
import json
import requester
import html_parser
import discord_bot
import disnake
import datadome


class Lbc:
    def __init__(self):
        self.filters = {"filters" : []}
        self.threads = []
        self.hfilters = open("config/lbc.json", "r+")

        self.hcookies = open("config/lbc_cookies.json", "r+")
        self.cookies = {}
        try:
            self.cookies = json.load(self.hcookies)
        except Exception as e:
            print(e)
            print("Couldn't fetch LBC cookies")

        if not self.load_filters():
            self.dump_filters()
        
        for filter in self.filters["filters"]:
            self.create_thread(filter)
    
    def add_filter(self, filter:dict, update_file:bool) -> bool:
        #if filter thread allready exists
        for thread in self.threads:
            if thread[0].name == filter["url"]:
                return False
        
        self.filters["filters"].append(filter)
        
        self.create_thread(filter)

        if update_file:
            self.dump_filters()
        return True

    def remove_filter(self, discord_channel:disnake.channel):
        #remove from file / memory
        for filter in self.filters["filters"]:
            if filter["discord_channel_id"] == discord_channel.id:
                self.filters["filters"].remove(filter)
                self.dump_filters()
                break

        #remove thread
        for thread in self.threads:
            if thread[0].name == str(discord_channel.id):
                thread[1] = True

        return True
    
    def load_filters(self) -> bool:
        try:
            self.filters = json.load(self.hfilters)
            return True
        except:
            return False

    def dump_filters(self):
        dumps = json.dumps(self.filters, indent=4)
        self.hfilters.seek(0)
        self.hfilters.write(dumps)
        self.hfilters.truncate()

    def create_thread(self, filter:dict, channel_obj:disnake.channel = None):
        #create thread
        #get channel object
        thread_index = len(self.threads)
        thread = Thread(name=filter["discord_channel_id"], target=self.filter_thread, args=(filter,thread_index))
        self.threads.append([thread,False])
        thread.start()

    def send_product(self, article:dict, channel_obj:disnake.channel):
        def is_valid_image_link(link: str) -> bool:
            """
            Check if a given link points to a valid image using regular expressions.

            Args:
                link (str): The URL of the image.

            Returns:
                bool: True if the link is a valid image, False otherwise.
            """
            if link == None or link == "":
                return False
            
            if "https" not in link:
                return False
            
            if "leboncoin.fr" not in link:
                return False

            return True  # It's a valid image link

        embed=disnake.Embed(title=article["title"], url=article["url"], color=0x0091ff)
        embed.set_image(url=article["img_src"] if is_valid_image_link(article["img_src"]) else "https://t4.ftcdn.net/jpg/04/70/29/97/360_F_470299797_UD0eoVMMSUbHCcNJCdv2t8B2g1GVqYgs.jpg")
        embed.add_field(name="Prix 💰", value=article["price"], inline=True)
        embed.add_field(name="Marque ®️", value=article["marque"], inline=True)
        embed.add_field(name="Ville 🏙️", value=article["ville"], inline=True)
        embed.add_field(name="Date 🕒", value=article["date"], inline=True)
        embed.add_field(name="Auteur 👤", value=article["author"], inline=True)
        embed.set_footer(text="BERRY Scraper v1.0")

        discord_bot.bot.loop.create_task(
            channel_obj.send(embed=embed)
        )

    def dump_cookies(self):
        dumps = json.dumps(self.cookies, indent=4)
        self.hcookies.seek(0)
        self.hcookies.write(dumps)
        self.hcookies.truncate()

    def filter_thread(self, filter:dict, thread_index:int):
        #vars
        max_id = 0
        local_max_id = 0
        count = 1
        dd_cookie = None
        url = filter["url"]
        discord_channel_id = str(filter["discord_channel_id"])
        fetched_dd_count = 0

        #get channel object
        channel_obj = None
        while channel_obj == None:
            channel_obj = discord_bot.bot.get_channel(filter["discord_channel_id"])
        
        embed=disnake.Embed(color=0x0091ff)
        embed.add_field(name="Filtre sous écoute :ballot_box_with_check: ", value=filter["url"], inline=False)
        discord_bot.bot.loop.create_task(channel_obj.send(embed=embed))

        while True and not self.threads[thread_index][1]:
            try:
                sleep(1)
                dd_cookie = None
                if discord_channel_id in self.cookies:
                    dd_cookie = self.cookies[discord_channel_id]
                (html, code) = requester.getHtml(url, dd_cookie)
                if code == 403:
                    if fetched_dd_count > 5:
                        print("Fetched to much time datadome cookie, killing thread")
                        break
                    fetched_dd_count += 1
                    self.cookies[discord_channel_id] = datadome.fetchCookie(filter["url"])
                    self.dump_cookies()
                    continue

                products = html_parser.GetProducts(html)
                if products == None:
                    continue

                local_max_id = 0
                for product in products:
                    if product['id'] > max_id and max_id != 0:
                        self.send_product(product, channel_obj)
                        count += 1
                    local_max_id =  max(local_max_id, product['id'])
                if local_max_id > max_id:
                    max_id = local_max_id
            except Exception as e:
                # #send error embed
                # embed=disnake.Embed(color=0xff0000)
                # embed.add_field(name="Erreur rencontrée :x:", value=str(e), inline=False)
                # discord_bot.bot.loop.create_task(channel_obj.send(embed=embed))

                # id = filter["discord_channel_id"]
                # channel = discord_bot.bot.get_channel(id).name
                # print(channel, "-> error:", e)
                # break
                pass 
        print(f"{channel_obj.name} -> Filter killed")

if __name__ == "__main__":
    print(__file__.split('\\')[-1],":",module_error_message)
    exit(1)
