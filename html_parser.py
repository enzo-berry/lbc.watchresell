from config.config import module_error_message

from bs4 import BeautifulSoup

def GetProducts(page_source):
    products_list = []

    html = page_source
    soup = BeautifulSoup(html, 'html.parser')

    lifestyle = 1
    # Mosaic view for lifestyle product
    div_all_products = soup.find("div", {"id": "mosaic_with_owner"})
    # List view for all other product
    if not div_all_products:
        div_all_products = soup.find(lambda tag: tag.name == 'div' and tag.get('class') == ['mb-lg'])
        lifestyle = 0
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

            # Marque only if lifestyle view
            if lifestyle == 1:
                marque = product_a_class.find("div", {"data-test-id": "ad-params-light"})
                product['marque'] = marque.text
            else:
                product['marque'] = None
            
            # Ville et date
            ville = product_a_class.find("span", {"class": "mr-[1.2rem] last:mr-none"})
            date = product_a_class.find("span", {"class": "relative inline-block w-full before:absolute before:right-full before:top-none before:hidden before:w-[1.2rem] before:text-center before:font-bold before:content-['·'] tiny:w-auto tiny:before:inline-block"})
            if ville:
                ville = ville.text
            if date:
                date = date.text
                
            product['ville'] = ville if ville else "non spécifié"
            product['date'] = date if date else "non spécifié"
        
            etat = product_a_class.find_all("span", attrs={"data-spark-component": "tag"})
            if etat:
                if len(etat) == 1:
                    product['etat'] = etat[0].text
                else:
                    # Lifestyle view, ignore the first "a la une" tag
                    product['etat'] = etat[1].text
            else:
                product['etat'] = "Main propre"

            #author
            author = product_a_class.find("div", {"class": "mb-md flex items-center gap-sm"})
            author = author.find("span")
            product['author'] = author.text if author else None


            products_list.append(product)
    
    return products_list

if __name__ == "__main__":
    print(__file__.split('\\')[-1],":",module_error_message)
    exit(1)