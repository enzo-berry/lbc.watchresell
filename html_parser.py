from config.config import module_error_message

from bs4 import BeautifulSoup

def GetProducts(page_source):
    products_list = []

    html = page_source
    soup = BeautifulSoup(html, 'html.parser')

    div_all_products = soup.find("div", {"id": "mosaic_with_owner"})
    if not div_all_products:
        print("Not found div_all_products")
        return None

    for product_div in div_all_products:
        product = {}

        product_a_class = product_div.findChildren("a" , recursive=False)
        #getting url
        if len(product_a_class) == 1:
            product_a_class = product_a_class[0]
            url = "https://www.leboncoin.fr" + product_a_class.get('href')
            id = int(url.split("/")[-1].split(".")[0])
            
            product['url'] = url
            product['id'] = id


            #title
            product_title = product_a_class.find("p", {"data-qa-id": "aditem_title"})
            if product_title:
                product_title = product_title.text
                product['title'] = product_title

            #price
            product_price = product_a_class.find("p", {"data-test-id": "price"})
            if product_price:
                product_price = product_price.text
            product['price'] = product_price
            
            # Image
            # Find the second image in product_a_class (you can complete this part)
            # For example, to find the second image source:
            image = product_a_class.find("img", {"alt": ""})
            product['img_src'] = image.get("src") if image else None

            # Marque
            marque = product_a_class.find("div", {"data-test-id": "ad-params-light"})
            product['marque'] = marque.text if marque else None

            # Ville et date
            parent_ville = product_a_class.find("div", {"class": "mr-md flex-1 min-w-0"})
            if parent_ville:
                parent_ville.find_all("span")
                ville = parent_ville.find_all("span")[1].text
                date = parent_ville.find_all("span")[2].text
                product['ville'] = ville
                product['date'] = date

            #author
            author = product_a_class.find("div", {"class": "flex items-center gap-sm mb-md"})
            author = author.find("span")
            product['author'] = author.text if author else None


            products_list.append(product)
    
    return products_list

if __name__ == "__main__":
    print(__file__.split('\\')[-1],":",module_error_message)
    exit(1)